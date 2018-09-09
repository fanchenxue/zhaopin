#!/usr/bin/env python
# encoding=utf-8

'''
@author: Francis

@contact: ryomawithlst@sina.com
@software: PyCharm
@file: export.py
@time: 2017/11/15
@license: (C) Copyright 2017

@desc:
'''
import re
from pymysql import connect,cursors
from zhaopin_itcast.settings import CITY, KEYWORDS
import hashlib
from concurrent import futures
import redis

def get_client(n=5):
    lt = []
    for i in range(n+1):
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=i)
        client = redis.Redis(connection_pool=pool)
        lt.append(client)
    return lt







def get_redis(db=10):
    import redis
    client = redis.StrictRedis(host="127.0.0.1", port=6379, db=db)
    return client


def get_data():
    sql = '''SELECT * FROM zhaopin.jobs_week_month '''
    db = connect(host='127.0.0.1', user='root', passwd='123456', db='zhaopin',
                               charset='utf8')

    cur = db.cursor(cursors.SSCursor)
    # cur = db.cursor()
    cur.execute(sql)
    return cur

# res = select_data()
# print(res.keys())
# for r in res.fetchall():
#     print(r)
# exit()


def input_redis(item,client):
    # redis_db = get_redis(db)
    # print(1)
    keys = ['id', 'url', 'city', 'keyword', 'source', 'filter', 'job_name', 'company_name', 'experience', 'education_background', 'number', 'office_address', 'category', 'keywords', 'salary', 'pub_date', 'description', 'company_size', 'company_area', 'updatetime']
    result = dict(zip(keys, item))
    result["repetition"] = False
    taskid = hashlib.sha1(result["url"].encode()).hexdigest()
    # print(taskid)
    client.hmset("jobs_%s"%taskid, result)





def repet_change():
    a = 0
    b = 0
    for key in redis.scan_iter("jobs_*"):
        item = redis.hgetall(key)
        item = {k.decode():v.decode() for k,v in item.items()}
        string = item["job_name"]+item["company_name"]+item["office_address"]+item["description"]
        sha256 = hashlib.sha256(string.encode()).hexdigest()
        ret = redis.sadd("check_repetition", sha256)
        if ret == 0:
            b += 1
            print("find one repetition")
            item["repetition"] = True
            redis.hmset(key, item)
        a += 1
        if a in range(0, 2000000, 1000):
            print(a)
    print(a)
    print(b)



def export_to_json():
    '''
    导出去重后的数据
    :param spider:
    :return:
    '''
    import json
    import re
    redis = get_redis()
    scan = redis.scan_iter
    citys = {}
    for city in CITY:
        citys[city] = {}
        for kw, filter in KEYWORDS:
            citys[city][kw] = {"count":0, "number": 0, "min_sum":0.0, "max_sum":0.0, "skip": 0}

    a = 1
    for key in scan("jobs_*"):
        task = redis.hgetall(key)
        if task["repetition"] == "False":
            number = 1
            if task["source"] == "zl":
                if u"若干" in task["number"].decode("utf-8"):
                    number = 3
                else:
                    number = int(task["number"][0])
            elif task["source"] == "qc":
                number = re.match(r".*?(\d+).*", task["number"])
                if number:
                    number = int(number.group(1))
                else:
                    number = 3
            a += 1
            print(task["city"].decode("utf-8"), task["keyword"].decode("utf-8"), key)
            if not citys[task["city"].decode("utf-8")].get(task["keyword"].decode("utf-8")):
                print("~~~~~~~~")
                continue
            citys[task["city"].decode("utf-8")][task["keyword"].decode("utf-8")]["number"] += number
            citys[task["city"].decode("utf-8")][task["keyword"].decode("utf-8")]["count"] += 1

            if "-" in task["salary"]:
                min, max = map(lambda x: re.findall(r"(\d+)", x)[0], task["salary"].split("-"))
                citys[task["city"].decode("utf-8")][task["keyword"].decode("utf-8")]["min_sum"] += int(min)
                citys[task["city"].decode("utf-8")][task["keyword"].decode("utf-8")]["max_sum"] += int(max)
            else:
                citys[task["city"].decode("utf-8")][task["keyword"].decode("utf-8")]["skip"] += 1

    print(a)
    for city in CITY:
        for kw, filter in KEYWORDS:
            print(city),
            print(kw),
            print(citys[city][kw]["count"]),
            print(citys[city][kw]["number"]),
            print(citys[city][kw]["min_sum"]),
            print(citys[city][kw]["max_sum"])
    with open("city.json", 'w') as f:
        f.write(json.dumps(citys))



if __name__ == '__main__':
    # from tqdm import tqdm
    cur = get_data()
    client = get_client()
    with futures.ThreadPoolExecutor(80) as executor:
        # executor.map(input_redis,cur)
        for n,item in enumerate(cur):
            # print(item)
            if n in range(0, 1000000, 1000):
                print(n)
            if n <= 500000:
                executor.submit(input_redis,item,client[0])
            elif 500000 < n <= 1000000:
                executor.submit(input_redis, item,client[1])
            elif  1000000< n <= 1500000:
                executor.submit(input_redis, item, client[2])
            else:
                executor.submit(input_redis, item, client[3])


    # repet_change()
    # export_to_json()






