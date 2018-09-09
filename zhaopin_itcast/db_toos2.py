from pymysql import connect

db = connect(host='172.17.0.113', user='itcast',passwd='itcast2017', db='spider_jobs', charset='utf8')

def db_delete():
    sql = "delete from jobs_week_39th where source = 'zl' limit 10000"
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
        print('删除成功')
    except Exception as e:
        db.rollback()
        print('删除失败')
        print(e)
if __name__ == '__main__':
    while True:
        db_delete()
