from pymysql import connect

db = connect(host='39.106.217.84', user='root', passwd='Lxcc198521394', db='zhaopin',
                               charset='utf8')
cur = db.cursor()

while True:
    sql = 'delete from jobs_week_test where source="zl" limit 10000'
    try:
        cur.execute(sql)
        db.commit()
        print('删除成功')
    except Exception as e:
        db.rollback()
        print('删除失败')
        print(e)
