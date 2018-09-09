from datetime import datetime, timedelta


def yesterday(days=7):
    now = datetime.now()
    yesterday = now - timedelta(days=days)
    y = str(yesterday.date())
    y = y.replace('-', '')
    return int(y), str(now).split(' ')[0]

def salary_format(sy):
        salary = sy
        if '千/月' in sy:
            salary = sy.replace('千/月','').split('-')
            salary = '-'.join([str(int(float(i)*1000)) for i in salary])
        elif '万/月' in sy:
            salary = sy.replace('万/月', '').split('-')
            salary = '-'.join([str(int(float(i) * 10000)) for i in salary])
        elif '万/年' in sy:
            salary = sy.replace('万/年', '').split('-')
            salary = '-'.join([str(int((float(i)/12)*10000)) for i in salary])
        elif '元/天' in sy:
            salary = sy.replace('元/天', '')
            salary = str(int(salary)*30)
            salary = salary+'-'+salary
        return salary
if __name__ == '__main__':
     a = [] or 's'
     print(a)