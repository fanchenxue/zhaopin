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
from sqlalchemy import create_engine
from zhaopin_itcast.settings import CITY, KEYWORDS
import hashlib

MYSQL_RESULT_CONF = 'mysql+pymysql://root:123456@127.0.0.1/zhaopin?charset=utf8'
def get_redis(db=10):
    import redis
    client = redis.StrictRedis(host="127.0.0.1", port=6379, db=db)
    return client

# redis = get_redis()

def get_data():
    sql = '''SELECT * FROM zhaopin.jobs_week_39_th limit 10'''
    # sql2 = '''select id from spider_jobs.jobs_week_1th where url="{0}"'''
    # sql3 = '''DELETE FROM spider_jobs.jobs_week_1th where id={0}'''

    conn = create_engine(MYSQL_RESULT_CONF)
    cur = conn.execute(sql)
    keys = cur.keys()
    print(keys)
get_data()
exit()
# def input_redis():
#
#     i = 0
#     for item in cur.fetchall():
#         result = dict(zip(keys, item))
#         result["repetition"] = False
#
#         taskid = hashlib.sha1(result["url"]).hexdigest()
#
#         redis.hmset("jobs_%s"%taskid, result)
#
#         i += 1
#         if i in range(0, 1000000, 1000):
#             print(i)
#
# input_redis()

def repet_change():
    a = 0
    b = 0
    for key in redis.scan_iter("jobs_*"):
        item = redis.hgetall(key)
        string = item["job_name"]+item["company_name"]+item["office_address"]+item["description"]
        sha256 = hashlib.sha256(string).hexdigest()
        ret = redis.sadd("check_repetition", sha256)
        if ret == 0:
            b += 1
            print("find one repetition")
            item["repetition"] = True
            redis.hmset(key, item)
        a += 1
        if a in range(0, 1000000, 1000):
            print(a)
    print(a)
    print(b)

repet_change()

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

export_to_json()

def export_to_csv(type):
    print(type,'ok')
    import pymongo
    from collections import OrderedDict
    mongo = pymongo.MongoClient(host="172.17.0.113", port=27017)
    database = mongo["spider_itcast"]
    sheet = database["37th_backup"]
    with open("./%s.json"%(type), 'r') as f:
        import json
        result = json.loads(f.read())
        result = OrderedDict(result)
        with open("./%s.csv"%(type), 'w') as f2:
            for city, kw in result.iteritems():
                # print(kw,)
                city = u'北京|010000'
                f2.write(city.encode("gbk"))
                f2.write("\n")
                for k, v in kw.iteritems():
                    print (k)
                    line = []
                    line.append(k)
                    jls = sheet.find_one({"data.location":city, "data.position":k})
                    # print list(jls)
                #     line.append(str(jls[0]["data"]["count"]+jls[1]["data"]["count"]++jls[2]["data"]["count"]))
                #     line.append(str(v["count"]))
                #     line.append(str(v["number"]))
                #     if v["count"] and v["count"] != v["skip"]:
                #         line.append(str(v["min_sum"]/(v["count"]-v["skip"])))
                #         line.append(str(v["max_sum"]/(v["count"]-v["skip"])))
                #     else:
                #         line.append("0")
                #         line.append("0")
                #     line = ','.join(line)
                #     f2.write(line.encode("gbk"))
                #     f2.write("\n")
                # f2.write("\n")

# if __name__ == '__main__':
#     pass







