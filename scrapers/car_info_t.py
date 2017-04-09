import re,random,requests,time,pymysql
from multiprocessing import Pool
from bs4 import BeautifulSoup
from ip_proxy.agents_setting import user_agent_list
from ip_proxy.agents_setting import xun_ips

class CarInfo:

    def __init__(self):
        self.user_agent_list = user_agent_list
        self.iplist=xun_ips

    # def test_ip(self,url,proxy=None):
    #     proxy=random.choice(self.iplist)
    #     try:
    #         response= requests.get(url,proxies=proxy)
    #         print('该ip代理%s可用'%proxy)
    #     except:
    #         pass
    #     return proxy

    def get_info(self,url,proxy=None,headers=None,num_retries=3):
        if proxy==None:
            headers = {'User-Agent':self.user_agent_list[0]}#本机headers
            try:
                web_data=requests.get(url, headers=headers,timeout=3)
                soup = BeautifulSoup(web_data.text, 'lxml')
                car_name = soup.select('div.dt-titbox > h1')[0].text
                print(headers,'\n',proxy,'\n',car_name)
            except:
                print('第1次请求失败')
                if num_retries>0:
                    time.sleep(3)
                    print('正进行倒数第%s次请求'%num_retries)
                    return self.get_info(url,num_retries-1)
                else:
                    print('开始使用代理')
                    return self.get_info(url,proxy=random.choice(self.iplist))
        else:
            try:
                headers=random.choice(self.user_agent_list[1:])
                proxy=random.choice(self.iplist)
                web_data = requests.get(url, headers=headers,proxies=proxy, timeout=3)
                soup = BeautifulSoup(web_data.text, 'lxml')
                car_name = soup.select('div.dt-titbox > h1')[0].text
                print(headers, '\n', proxy, '\n', car_name)
            except:
                if num_retries>0:
                    time.sleep(3)
                    print('正进行使用代理%s进行倒数第%s请求' %(proxy,num_retries) )
                    return self.get_info(url,proxy,num_retries-1)
                else:
                    print('该链接%s失效'%url,'填入空数据')
                    pass

        # soup = BeautifulSoup(web_data.text, 'lxml')
        # car_name = soup.select('div.dt-titbox > h1')[0].text
        # time.sleep(1+random.random())
        # print(car_name)
        # # h_response = requests.get('http://httpbin.org/get', headers=headers).text
        # # print(json.loads(h_response)['headers']['User-Agent'],'\n', json.loads(h_response)['origin'])
        # web_data = requests.get(url, headers=headers,timeout=3)
        # soup = BeautifulSoup(web_data.text, 'lxml')
        # car_name = soup.select('div.dt-titbox > h1')[0].text
        # time.sleep(1+random.random())
        # print(car_name)


test=CarInfo()


coon = pymysql.connect(host='127.0.0.1', user='root', password='123456',
                        port=3306, db='guazi', charset='utf8')
cur = coon.cursor()
cur.execute('select url from car_url where number<1000')
urllist = cur.fetchall()
url_list = []



for url in urllist:
    url = url[0]
    url_list.append(url)
#
# if __name__ == '__main__':
#     pool=Pool()
#     pool.map(test.get_info,url_list)
#
count=1
for url in urllist:
    url = url[0]
    print(count)
    test.get_info(url)
    count+=1