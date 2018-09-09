from pymysql import connect
from threading import Thread,Lock
from twisted.enterprise import adbapi
from twisted.internet import reactor


db = connect(host='172.17.0.113', user='itcast',passwd='itcast2017', db='spider_jobs', charset='utf8')
cur = db.cursor()

sql = 'select `url`,`city`,`keyword`,`source`,`filter`,`job_name`,`company_name`,`experience`,`education_background`,`number`,`office_address`,`category`,`keywords`,`salary`,`pub_date`,' \
                  '`description`,`company_size`,`company_area`,`updatetime` from `jobs_week_39th-bak` limit 2000'


sql_insert = 'insert into `jobs_week_test`(`url`,`city`,`keyword`,`source`,`filter`,`job_name`,`company_name`,`experience`,`education_background`,`number`,`office_address`,`category`,`keywords`,`salary`,`pub_date`,' \
                  '`description`,`company_size`,`company_area`,`updatetime`) ' \
                  'VALUES({})'.format(',%s'*19).replace('(,','(')
cur.execute(sql)
res = cur.fetchall()


def insert_db(data):
    db = connect(host='172.17.0.113', user='itcast', passwd='itcast2017', db='spider_jobs', charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql_insert,data)
        db.commit()
        print('成功')
    except Exception as e:
        db.rollback()
        print('失败')
    finally:
        cur.close()
        db.close()


class MysqlThreed(Thread):
    def __init__(self,data):
        super().__init__()
        self.data = data
    def run(self):
        lock = Lock()
        with lock:
            while self.data:
                d = self.data.pop()
                insert_db(d)





if __name__ == '__main__':
    data = list(res)
    lt = []
    for i in range(50):
        t = MysqlThreed(data)
        t.start()
        lt.append(t)
    for i in lt:
        i.join()
