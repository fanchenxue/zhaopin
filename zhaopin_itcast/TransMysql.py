# -*- coding: utf-8 -*-
import json
import redis  # pip install redis
import pymysql
from concurrent import futures
from scrapy import spider


def main(table):
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='47.93.254.164', port = 6379,password='Lxcc198#!', db = 2)
    # 指定mysql数据库
    # mysqlcli = pymysql.connect(host='172.17.0.113', user='itcast',passwd='itcast2017', db='spider_jobs', charset='utf8')
    mysqlcli = pymysql.connect(host='39.106.217.84', user='root', passwd='Lxcc198521394', db='zhaopin',
                               charset='utf8')
    # 无限循环
    while True:
        source, data = rediscli.blpop(['zhilian:items','qiancheng:items','lagou:items','liepin:items']) # 从redis里提取数据

        item = json.loads(data.decode('utf-8')) # 把 json转字典

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            sql = 'insert into `{}`(`url`,`city`,`keyword`,`source`,`filter`,`job_name`,`company_name`,`experience`,`education_background`,`number`,`office_address`,`category`,`keywords`,`salary`,`pub_date`,' \
                  '`description`,`company_size`,`company_area`,`updatetime`) ' \
                  'VALUES({})'.format(table,',%s'*19).replace('(,','(')
            # sql = sql.format(**item)

            data = (item.get('url',''),item.get('city',''), item.get('keyword',''), item.get('source',''),
                    item.get('filter',''), item.get("job_name",''), item.get("company_name",''),item.get("experience",''),
                    item.get("education_background",''), item.get("number",''), item.get("office_address",''),item.get("category",''),
                    item.get("keywords",''), item.get("salary",''), item.get("pub_date",''), item.get("description",''), item.get("company_size",''), item.get("company_area",''), item.get("updatetime",''))
            cur.execute(sql,data)
            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
            print ("插入成功")
        except pymysql.Error as e:
            # pass
            mysqlcli.rollback()
            print ("插入错误" ,str(e))

if __name__ == '__main__':
    with futures.ThreadPoolExecutor(3) as executor:
        for i in range(3):
            executor.submit(main,'jobs_week_test')