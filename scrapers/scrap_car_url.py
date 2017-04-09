import random
import time
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from scrapers.car_info import get_car_info
import pymysql


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
coon = pymysql.connect(host='127.0.0.1',user='root',password='123456',port=3306,db='guazi',charset='utf8')
cur = coon.cursor()

def all_car_url(start_url,page):
    count=0
    webdata=requests.get(start_url+'o'+page+'/',headers=headers)
    soup=BeautifulSoup(webdata.text,'lxml')
    car_urls=soup.select('p.infoBox > a')
    for car_url in car_urls:
        count+= 1
        car_url='https://www.guazi.com'+car_url.get('href')
        print(40*(int(page)-1)+count,'爬取 %s'%car_url)
        cur.execute("insert into car_url(number,url) value(%s,%s)",(40*(int(page)-1)+count,car_url))
        coon.commit()
        # get_car_info(car_url)
        #time.sleep(1)


for page in range(2711,2715):
    print("正在获取第%s页"%page)
    all_car_url('https://www.guazi.com/www/buy/',str(page))
    time.sleep(1.7+random.random())


cur.close()
coon.close()


