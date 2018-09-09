from pymysql import connect
from twisted.enterprise import adbapi
from twisted.internet import reactor


db = connect(host='172.17.0.113', user='itcast',passwd='itcast2017', db='spider_jobs', charset='utf8')
cur = db.cursor()

sql = 'select `url`,`city`,`keyword`,`source`,`filter`,`job_name`,`company_name`,`experience`,`education_background`,`number`,`office_address`,`category`,`keywords`,`salary`,`pub_date`,' \
                  '`description`,`company_size`,`company_area`,`updatetime` from `jobs_week_test`'


sql_insert = 'insert into `jobs_week_39th`(`url`,`city`,`keyword`,`source`,`filter`,`job_name`,`company_name`,`experience`,`education_background`,`number`,`office_address`,`category`,`keywords`,`salary`,`pub_date`,' \
                  '`description`,`company_size`,`company_area`,`updatetime`) ' \
                  'VALUES({})'.format(',%s'*19).replace('(,','(')
cur.execute(sql)
res = cur.fetchall()


def insert_db(data):
    try:
        cur.executemany(sql_insert,data)
        db.commit()
        print('成功')
    except Exception as e:
        db.rollback()
        print('失败')
        print(e)


if __name__ == '__main__':
    n = 10000
    data = [res[i:i + n] for i in range(0, len(res), n)]
    for d in data:
        insert_db(d)