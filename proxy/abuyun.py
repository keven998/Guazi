# 代理ip的测试

import requests,time
from multiprocessing import Pool
from datetime import datetime
# 要访问的目标页面
targetUrl = "https://www.guazi.com/baotou/16851176b3aabf9dx.htm"
# targetUrl = "http://proxy.abuyun.com/switch-ip"
# targetUrl = "http://proxy.abuyun.com/current-ip"

# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9010"

# 代理隧道验证信息，个人代理隧道，不公开了
proxyUser = "H751819F41A8****"
proxyPass = "868FD8389E47****"

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

def get_response(i):
    resp = requests.get(targetUrl, proxies=proxies)
    # time.sleep(0.1)
    print(i, resp)

if __name__ == '__main__':
    start_time=datetime.now()
    pool=Pool()
    pool.map(get_response,range(1,500))
    end_time = datetime.now() - start_time
    print(end_time)
    # print(resp.status_code)
    # print(resp.text)