# !/usr/bin/python
# encoding:utf-8
import argparse
import sys
sys.path.append('/home/deployer/ec_scripts/SQL')
#import vvip_cus
import database_conf
import collections
import copy
import xlwt
import SQL
import pymysql
from linkage.utils import utils
import json
import subprocess
import datetime
import commands
reload(sys)
sys.setdefaultencoding("utf-8")

class use_sql(object):
    """
    汇总各组返回信息，生成excel文件
    """
    def __init__(self):
        self.cus_node = []
        self.wbk = xlwt.Workbook(encoding='utf-8')
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 2
        self.style_red = xlwt.XFStyle()
        self.style_red.pattern = pattern
        self.sql_result = {}          # 存放数据库查询结果

    def mysqlExecSql(self, pool):
        """
        查询数据库通过project_id获取nova.quotas中信息（deleted=0,用户配额信息）

        """
        dataconf = database_conf.ec_conf(pool)
        # hosts = str_input
        if len(pool) > 0:
            ec_uuid = SQL.ec_hosts_get_nodes_info()
            self.sql_result['result'] = utils.execsql(sql=ec_uuid, databaseconf=dataconf)
        for i in self.sql_result['result']:
	    print '\n############################'
            for key, value in i.items():
                if str(key) == '规格':
                    f = json.loads(str(value))
                    flavor = f['cur']['nova_object.data']['name']
                    print '%-20s' % str(key), ' : ', str(flavor)
                else:
                    print '%-20s'%str(key), ' : ', str(value)

def argsAnalysis():
    """
    输入参数
    """
    parser = argparse.ArgumentParser(prog='sql tools', description='查询资源池中所有虚机信息',
                                     epilog='Contact us with email: xxxx')
    parser.add_argument('--pool', help='choose pool')
    # parser.add_argument('--cli_input', help='the input info')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    """
    入口，通过project_id获取quotas表中信息
    """
    args = argsAnalysis()
    pool = args.pool
    sql = use_sql()
    status, host = commands.getstatusoutput('hostname')
    if pool in host:
        sql.mysqlExecSql(pool)


