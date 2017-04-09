import pymysql
import requests,time,os,winsound
from bs4 import BeautifulSoup
from proxy.agents_setting import user_agent_list
import random
from datetime import datetime
from multiprocessing import Pool

proxyHost = "proxy.abuyun.com"
proxyPort = "9010"
# 代理隧道验证信息,个人信息，不公开了
proxyUser = "H751819F41*****"
proxyPass = "868FD8389E47*****"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

class Guazi():
    def __init__(self):
        self.coon = pymysql.connect(host='127.0.0.1', user='root', password='123456',
                               port=3306, db='guazi', charset='utf8')
        self.cur = self.coon.cursor()
        self.cur.execute('select url from car_url where number>=106001 and number<=108560')
        self.urllist = self.cur.fetchall()

    def get_url_list(self):
        url_list = []
        for url in self.urllist:
            url = url[0]
            url_list.append(url)
        return url_list

    def random_head(self):
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, sdch",
                   "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
                   "Host": "www.guazi.com",
                   "Referer": "https://www.guazi.com/www/buy/",
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": random.choice(user_agent_list) }
        return headers


    def get_car_info(self,detail_url,num_retries=1):
        # time.sleep(1.5+random.random())
        try:
            web_data=requests.get(detail_url,self.random_head(),proxies=proxies,timeout=5)
            soup=BeautifulSoup(web_data.text,'lxml')
            print(detail_url, '访问成功')
            try:
                car_name=soup.select('div.dt-titbox > h1')[0].text
                second_price = soup.select('div.pricebox > span.fc-org.pricestype > b')[0].text.replace('¥','')+'w'
                try:
                    new_price = soup.select('div.pricebox > span.f14 > font')[0].text.replace('万','')+'w'
                except:
                    try:
                        new_price=soup.find_all('a',{'class':'stipul-btn stipul-btn-gray'})[0].text
                        print(new_price)
                    except:
                        new_price='无新车价格'
                det_table = soup.select('div.det-sumright.appoint > ul > li > b')
                license_time = det_table[0].text
                mile = det_table[1].text
                biansu = det_table[2].text
                standard = det_table[3].text
                card_adr = det_table[4].text
                test_report = soup.select('div.detect-txt')[0].text
                owner_des = soup.select('#base > p')[0].text
                owner_id = soup.select('#base > ul > li.owner')[0].text.split('|\n')[1].strip()
                city = soup.select('div.c2city > a > span')[0].text.split()[0]
                owner_adr = soup.select('#base > ul > li.owner')[0].text.split('|\n')[2].strip()
                brand = soup.select('div.crumbs > a')[2].text.split(city)[1].replace('二手车', '')
                sql = '''insert into car_info(品牌,车型,二手价,新车价,上牌时间,里程,变速箱,排放标准,上牌地,检测报告,车主描述,车主身份,车主地址,详情链接)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                print('提取数据成功')
                try:
                    self.cur.execute(sql,
                                [brand,car_name,second_price,new_price,license_time,mile,biansu,standard,card_adr,test_report,owner_des,owner_id,city+owner_adr,detail_url])
                    self.coon.commit()
                    print('插入数据库成功')
                except:
                    print('插入数据库——失败——')
                    pass
            except:
                print('提取数据——失败——')
                pass
        except:
            print(detail_url,'第%s次访问——失败——'%num_retries)
            if num_retries<2:
                self.get_car_info(detail_url,num_retries+1)
            elif num_retries<3:
                time.sleep(2)
                self.get_car_info(detail_url,num_retries + 1)
            else:
                winsound.Beep(500,800)
                print(detail_url,'试了三次啦，真的不能访问！！！！！！！！')
                pass

if __name__ == '__main__':
    # start_time=datetime.now()
    guazi = Guazi()
    pool=Pool(8)
    pool.map(guazi.get_car_info,guazi.get_url_list())
    # end_time = datetime.now() - start_time
    # print(end_time)
    guazi.cur.close()
    guazi.coon.close()
    os.system("5.mp3")






