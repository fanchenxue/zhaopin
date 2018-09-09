from pymysql import connect


def ZL_Salary():
    db = connect(host='172.17.0.113', user='itcast',passwd='itcast2017', db='spider_jobs', charset='utf8')
    cur = db.cursor()
    while True:
        sql = 'select salary,id from jobs_week_39th where source="zl" and salary like "%K%" limit 5000'
        cur.execute(sql)
        res = cur.fetchall()
        if 'K' not in str(res):
            break
        data = map(salary_format,res)
        try:
            sql_update = 'update jobs_week_39th set salary=%s where id=%s'
            cur.executemany(sql_update,data)
            db.commit()
            print('更新成功')
        except Exception as e:
            db.rollback()
            print('更新失败')
            print(e)

def salary_format(tp):
    lt = list(tp)
    sy = lt[0]
    if 'K' in sy and '-' in sy:
        salary = sy.split('-')
        salary = '-'.join([str(int(float(i.replace('K',''))*1000)) for i in salary])
        lt[0] = salary
    elif 'K以下' in sy:
        salary = str(int(float(sy.replace('K以下',''))*1000))
        lt[0] = salary
    return lt

if __name__ == '__main__':
    ZL_Salary()
