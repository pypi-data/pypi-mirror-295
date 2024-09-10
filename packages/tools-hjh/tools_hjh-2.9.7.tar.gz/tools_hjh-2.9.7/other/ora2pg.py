# coding:utf-8
from tools_hjh import DBConn, Tools, ProcessPool
from tools_hjh.Tools import locatdate
from tools_hjh import Log
from tools_hjh import ThreadPool
from tools_hjh import OracleTools
import time
import gc
from math import ceil
import sys

date = locatdate()
Tools.rm(date + '.log')
log = Log(date + '.log')

conf = Tools.cat('ora2pg.conf')
conf_map = {}
for line in conf.split('\n'):
    if '=' in line and '#' not in line:
        key = line.split('=')[0].strip()
        val = line.split('=')[1].strip()
        conf_map[key] = val

smallest_object = conf_map['smallest_object']
if_truncate = conf_map['if_truncate']
if_only_scn = conf_map['if_only_scn']

src_db_type = conf_map['src_db_type']
src_ip = conf_map['src_ip']
src_port = int(conf_map['src_port'])
src_database = conf_map['src_db']
src_read_username = conf_map['src_read_username']
src_read_password = conf_map['src_read_password']
src_schema = conf_map['src_schema']

src_tables = conf_map['src_tables'].replace(',', "','").upper()

dst_db_type = conf_map['dst_db_type']
dst_ip = conf_map['dst_ip']
dst_port = int(conf_map['dst_port'])
dst_database = conf_map['dst_db']
dst_username = conf_map['dst_username']
dst_password = conf_map['dst_password']
dst_schema = conf_map['dst_schema']

parallel_table_num = int(conf_map['parallel_table_num'])
table_parallel_num = int(conf_map['table_parallel_num'])
save_parallel_num = int(conf_map['save_parallel_num'])

commit_num = int(conf_map['commit_num'])
myscn = conf_map['scn']

report = {}

try:
    only_report = sys.argv[1]
except:
    only_report = None
try:
    only_report_scn = sys.argv[2]
except:
    only_report_scn = None


# 主控制程序
def main():
    if only_report == None:
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, options='-c search_path=' + dst_schema + ',public')
            
        # 查出表清单
        if len(src_tables) > 0:
            select_tables_sql = "select table_name from dba_tables where owner = '" + src_schema.upper() + "' and table_name in('" + src_tables + "') and table_name != 'CHAINED_ROWS' order by 1"
        else:
            select_tables_sql = "select table_name from dba_tables where owner = '" + src_schema.upper() + "' and table_name != 'CHAINED_ROWS' order by 1"
        tables = src_db.run(select_tables_sql).get_rows()
        
        # 清理表
        if if_truncate == 'true':
            for table_mess in tables:
                dst_conn = dst_db.dbpool.connection()
                src_table = table_mess[0]
                truncate_table_sql = 'truncate table ' + src_table + ' cascade'
                try:
                    dst_cur = dst_conn.cursor()
                    dst_cur.execute(truncate_table_sql)
                    dst_conn.commit()
                    log.info(truncate_table_sql)
                except Exception as _:
                    log.warning(truncate_table_sql, str(_))
                finally:
                    dst_cur.close()
                
        # 获取scn，如果需要
        if if_only_scn == 'true' and len(myscn) == 0:
            scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
        elif if_only_scn == 'true' and len(myscn) > 0:
            scn = myscn
        else:
            scn = None
        
        # 多线程启动表分析程序
        tp = ThreadPool(parallel_table_num, while_wait_time=0.1)
        for table_mess in tables:
            src_table = table_mess[0]
            tp.run(run_table, (src_table, scn))
        tp.wait()
        
        src_db.close()
        dst_db.close()
        
        # 获取输出报告
        get_report()
        
    elif only_report == 'report':
        get_report(only_report_scn)


# 表分析程序
def run_table(src_table, scn):
    # 获取连接
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
     
    # 如果没有scn，则此处获取
    if scn is None:
        scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
    
    # 获取表元数据信息
    mess_map = OracleTools.get_table_metadata(src_db, src_schema, src_table, partition=True)
    
    # 获取表数量，用于对数
    count_sql = 'select count(1) from ' + src_schema + '."' + src_table + '" as of scn ' + scn
    src_num = src_db.run(count_sql).get_rows()[0][0]
    report[src_table.lower()] = [src_num, None]

    # 遍历分区子分区，多进程分配查询任务及后续任务
    tp = ProcessPool(table_parallel_num, while_wait_time=0.1)
    partition_mess = mess_map['partition']
    if partition_mess is not None and smallest_object != 'table':
        for partition in partition_mess['partitions']:
            partition_name = partition['name']
            subpartitions = partition['subpartitions']
            if len(subpartitions) > 0 and smallest_object == 'subpartition':
                for subpartition in subpartitions:
                    subpartition_name = subpartition['name']
                    mess = src_schema + '."' + src_table + '" subpartition(' + subpartition_name + ')'
                    tp.run(get_data_from_oracle, (src_table, mess, scn))
            else:
                mess = src_schema + '."' + src_table + '" partition(' + partition_name + ')'
                tp.run(get_data_from_oracle, (src_table, mess, scn))
    else:
        mess = src_schema + '."' + src_table + '"'
        page_num = ceil(src_num / commit_num)
        if page_num <= table_parallel_num:
            tp.run(get_data_from_oracle, (src_table, mess, scn))
        else:
            page_rn = ceil(src_num / table_parallel_num)
            for page in range(1, table_parallel_num + 1):
                tp.run(get_data_from_oracle, (src_table, mess, scn, page, page_rn))
    tp.wait()
    
    src_db.close()

        
def get_data_from_oracle(table_name, mess, scn, page=None, page_rn=None): 
    try:
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        
        if page is None:
            select_sql = 'select /*+ FIRST_ROWS */ *  from ' + mess + ' as of scn ' + scn
        else:
            cols_tuple = src_db.run('select * from ' + mess + ' as of scn ' + scn + ' where rownum = 1').get_cols()
            cols_str = ''
            for col in cols_tuple:
                cols_str = cols_str + col + ','
            cols_str = cols_str[:-1]
            select_sql = '''
                select /*+ parallel(''' + str(page_rn) + ''') */ ''' + cols_str + ''' from (
                    select t.*,rownum rn 
                    from ''' + mess + ''' 
                    as of scn ''' + str(scn) + ''' t
                    where rownum <= ''' + str(page) + ''' * ''' + str(page_rn) + '''
                ) where rn <= ''' + str(page) + ''' * ''' + str(page_rn) + '''
                and rn > ''' + str(page - 1) + ''' * ''' + str(page_rn) + '''
            '''
            
        rs = src_db.run(select_sql)
        cols = rs.get_cols_description()
        
        i = 1
        tp = ThreadPool(save_parallel_num, while_wait_time=0.1)
        while True:
            if page is None:
                my_mess = mess + '(' + str(i) + ')'
            else:
                my_mess = mess + '(' + str(page) + '-' + str(i) + ')'
            time_start = time.time()
            rows = rs.get_rows(commit_num)
            select_time = time.time() - time_start
            if len(rows) == 0:
                break
            tp.run(save_to_pg, (table_name, rows, cols, my_mess, select_time, scn))
            i = i + 1
            if len(rows) < commit_num:
                break
            del rows
            gc.collect()
        tp.wait()
    except Exception as _:
        log.error('get_data_from_oracle', mess, str(_))
    finally:
        src_db.close()


def save_rows_to_file(mess, scn, rows):
    pass


def get_file_rows_to_pg():
    pass

        
def save_to_pg(table_name, rows, cols, mess, select_time, scn):
    # pid = os.getpid()
    time_start = time.time()
    # 获取连接
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, options='-c search_path=' + dst_schema + ',public')
    
    wenhaos = ''
    for _ in cols:
        wenhaos = wenhaos + '?,'
    wenhaos = wenhaos[0:-1]
    insert_sql = 'insert into ' + table_name + ' values(' + wenhaos + ')'
    
    try:
        num = dst_db.pg_copy_from(table_name.lower(), rows, cols)
        num = str(num) + '(copy)' 
    except Exception as _:
        log.warning(mess, str(_))
        try:
            num = dst_db.run(insert_sql, rows)
            if num == -1:
                raise Exception('unknown error, num = -1')
            num = str(num) + '(insert)' 
        except Exception as _:
            log.error(mess, str(_))
            return
    finally:
        del rows
        gc.collect()
        dst_db.close()

    save_time = time.time() - time_start
    log.info(mess, num, str(round(select_time, 2)) + 's', str(round(save_time, 2)) + 's', 'scn=' + scn)


def get_report(only_report_scn=None):
    tp = ThreadPool(8)

    def count(db, sql, table_name):
        try:
            num = int(db.run(sql).get_rows()[0][0])
        except Exception as _:
            num = 0
        report[table_name][1] = num
        log.info('report', report[table_name][0] == report[table_name][1], table_name, report[table_name][0], report[table_name][1])
    
    def count2(src_db, src_sql, dst_db, dst_sql, table_name):
        try:
            src_num = int(src_db.run(src_sql).get_rows()[0][0])
        except Exception as _:
            src_num = 0
        try:
            dst_num = int(dst_db.run(dst_sql).get_rows()[0][0])
        except Exception as _:
            dst_num = 0
            
        report[table_name] = [src_num, dst_num]
        log.info('report', report[table_name][0] == report[table_name][1], table_name, report[table_name][0], report[table_name][1])
    
    if only_report_scn is None:
        log.info('Generating report')
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8, options='-c search_path=' + dst_schema + ',public')
        error_table = ''
        
        for k in report:
            table_name = k.replace('"', '')
            dst_sql = 'select count(1) from ' + table_name
            tp.run(count, (dst_db, dst_sql, table_name))
        tp.wait()
        
        for k in report:
            if  report[k][0] != report[k][1]:
                error_table = error_table + k + ','
                
        log.info('error_table', error_table)
        dst_db.close()
            
    else:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8, options='-c search_path=' + dst_schema + ',public')
        
        # 查出表清单
        if len(src_tables) > 0:
            select_tables_sql = "select table_name from dba_tables where owner = '" + src_schema.upper() + "' and table_name in('" + src_tables + "') and table_name != 'CHAINED_ROWS' order by 1"
        else:
            select_tables_sql = "select table_name from dba_tables where owner = '" + src_schema.upper() + "' and table_name != 'CHAINED_ROWS' order by 1"
        tables = src_db.run(select_tables_sql).get_rows()
        
        error_table = ''
        for table_mess in tables:
            src_table = table_mess[0]
            src_sql = 'select /*+ parallel(8) */ count(1) from ' + src_schema + '."' + src_table + '" as of scn ' + only_report_scn
            dst_sql = 'select count(1) from ' + src_table
            tp.run(count2, (src_db, src_sql, dst_db, dst_sql, src_table))
        tp.wait()
            
        for k in report:
            if report[k][0] != report[k][1]:
                error_table = error_table + k + ','
                
        log.info('error_table', error_table)
        src_db.close()
        dst_db.close()

            
if __name__ == '__main__': 
    main()
