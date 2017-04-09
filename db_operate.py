import pymysql



def insert_data():
    coon = pymysql.connect(host='127.0.0.1',user='root',
                           password='123456',port=3306,db='guazi',charset='utf8')
    cur = coon.cursor()
    cur.execute("insert into test(id,url) values (1,'www.baidu.com')")
    coon.commit()
    print(cur.fetchall())
    cur.close()
    coon.close()
