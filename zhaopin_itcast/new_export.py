from pymysql import connect,cursors
# from zhaopin_itcast.settings import CITY, KEYWORDS
import hashlib
from threading import Thread,Lock
from queue import Queue
import redis,time


def get_client(host="127.0.0.1",db=0):
    pool = redis.ConnectionPool(host=host, port=6379, db=db)
    client = redis.Redis(connection_pool=pool)
    return client


def get_data():
    sql = '''SELECT * FROM zhaopin.jobs_week_month'''
    db = connect(host='127.0.0.1', user='root', passwd='123456', db='zhaopin',
                               charset='utf8')
    cur = db.cursor(cursors.SSCursor)
    cur.execute(sql)
    return cur


class Input_Redis(Thread):
    _dup = set()
    _keys = ['id', 'url', 'city', 'keyword', 'source', 'filter', 'job_name', 'company_name', 'experience',
            'education_background', 'number', 'office_address', 'category', 'keywords', 'salary', 'pub_date',
            'description', 'company_size', 'company_area', 'updatetime']
    redis_cli = get_client()
    def __init__(self,mysql_Q,taskid_Q):
        self.mysql_Q = mysql_Q
        self.taskid_Q = taskid_Q
        super().__init__()
    def run(self):
        while self.mysql_Q.qsize():
            item = self.mysql_Q.get()
            result = dict(zip(self._keys, item))
            taskid = hashlib.sha1(result["url"].encode()).hexdigest()
            if taskid not in self._dup:
                self.redis_cli.hmset("url_%s"%taskid, result)
                self._dup.add(taskid)
                self.taskid_Q.put(taskid)
                print('存入url_%s'%taskid)
            else:
                print('重复url:%s'% result["url"])

class De_Dup(Thread):
    _redis_cli = get_client()
    redis_cli = get_client(db=1)
    def __init__(self,taskid_Q,threads):
        self.taskid_Q = taskid_Q
        self.threads = threads
        super().__init__()
    def run(self):
        lock = Lock()
        while self.threads or not self.taskid_Q.empty():
            for thread in self.threads:
                if not thread.is_alive():
                    with lock:
                        self.threads.remove(thread)
            key = self.taskid_Q.get()
            key = "url_%s"%key
            with self._redis_cli.pipeline() as pipe:
                pipe.hgetall(key)
                pipe.delete(key)
                item = pipe.execute()[0]
            item = {k.decode(): v.decode() for k, v in item.items()}
            st = item["job_name"]+item["company_name"]+item["office_address"]+item["description"]
            taskid = hashlib.sha256(st.encode()).hexdigest()
            self.redis_cli.hmset("content_%s" % taskid, item)
            self.taskid_Q.task_done()
            print('去重:%s' % taskid)


def mysqlQ(mysql_Q):
    cur = get_data()
    for c in cur:
        mysql_Q.put(c)

def main(max=30):
    mysql_Q = Queue()
    taskid_Q = Queue()

    t = Thread(target=mysqlQ,args=(mysql_Q,))
    t.start()
    time.sleep(1)
    threads = []

    for i in range(max):
        t = Input_Redis(mysql_Q,taskid_Q)
        t.start()
        threads.append(t)


    for i in range(max):
        t = De_Dup(taskid_Q,threads)
        t.start()

if __name__ == '__main__':
    main()


