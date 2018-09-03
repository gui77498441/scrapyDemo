#动态爬取代理
import requests
import random
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Queue,Process
import re
import os
import threading




# header = {
#             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#             'Accept-Encoding':'gzip, deflate',
#             'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
#             'Accept-Language':'zh-CN,zh;q=0.9'
#         }
# # url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
# # html = requests.get(url,headers = header).text
# # open('test.txt','w').write(html)
# # soup = BeautifulSoup(html,'lxml')
# # content = soup.findAll('pre')
# # print(content)

# # exit()

# proxy={
#             'https':'167.99.236.75:8080'
#        }
# #code =requests.get('https://read.douban.com/kind/190?start=60',headers = header,proxies=proxy).status_code
# code =requests.get('http://www.baidu.com/',headers= header,proxies=proxy,verify=False,timeout=2).status_code
# print(str(code))
# exit()









class Proxies(object):
    def __init__(self):
        self.proxies = []
        self.verifyProxies = []
        self.header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Accept-Language':'zh-CN,zh;q=0.9'
        }
        self.get_proxies()
        self.verify_proxies()

        

    #爬取代理
    def get_proxies(self):
        with open('test.txt','r') as f:
            lines = f.readlines()
        for line in lines:
            protocol = re.findall(r'"type": "(.+?)",',line)[0] + "://"
            if 'https' in protocol:
                port = re.findall(r'"port": (.+?),',line)[0]
                host = re.findall(r'"host": "(.+?)",',line)[0]
                tmp = []
                tmp.append(host)
                tmp.append(port)
                self.proxies.append(protocol + ':'.join(tmp) )
            

    #利用多线程来验证代理是否可用
    def verify_proxies(self):
        old_queue = Queue()
        new_queue = Queue()
        works = []
        for _ in range(10):
            works.append(threading.Thread(target = self.verifyOneProxy,args=(old_queue,new_queue)))
        for work in works:
            work.setDaemon(True)
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        print("join finished")
        while 1:
            try:
                self.verifyProxies.append(new_queue.get(timeout=1))
            except:
                break
        print('verify_proxies done')

    
    def verifyOneProxy(self,old_queue,new_queue):
        while 1:    
            proxy = old_queue.get(block=True,timeout=1)
            if proxy == 0:
                break
            #protocol = 'https' if 'https' in proxy else 'http'
            protocol = proxy.split('://')[0]
            ipport = proxy.split('://')[1]
            proxies = {protocol:ipport}
            try:
                code = requests.get('http://www.baidu.com',proxies=proxies,timeout=2).status_code
                if code == 200:
                    new_queue.put(proxy)
                else:
                    print(str(code))
            except:
                print("error")
                
if __name__ == '__main__':
    a = Proxies()
    with open('proxies.txt','a') as f:
        for item in a.verifyProxies:
            f.write(item+'\n')
    
