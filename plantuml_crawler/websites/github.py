import requests
import json
import math
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

#代理服务器

proxyHost = "114.99.134.178"
proxyPort = "3617"
"http://114.99.134.178:3617"
proxyMeta = "http://%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
}

proxies = {
    "http" : "101.32.251.31:10488",
    # "https" : "http://47.242.190.60:13294"
}

web_url = "https://github.com"
class Spider:
    # 使用
    headers = {'User-Agent':str(UserAgent().random)}
    # 获取搜索参数
    def __init__(self,key,language,limit):
        self.key = key
        self.limit = int(limit)
        self.language = language
        print("this is github's Spider:{},{}".format(key,limit))
    
    # 爬取网页链接
    def crawl_link(self):
        
        # 存储爬取到的名字和下载链接和星数
        self.list = []
        # 计算爬取页数
        page_nums = math.ceil(self.limit/10.0)
        print(page_nums)
        #
        page_num = 2
        # for page_num in range(1,page_nums):
        # 请求参数
        params = {
            'p': page_num,
            'l': self.language,
            'q': self.key,
            'type': 'Repositories'
        }
        # 请求网址
        url = web_url + '/search'
        # res = requests.get(url,params=params,headers=self.headers,proxies=proxies,timeout=6)
        res = requests.get(url,params=params,headers=self.headers,timeout=6)
        print(res.status_code)
        soup = BeautifulSoup(res.text,'html.parser')
        items = soup.find_all('li',class_='repo-list-item')
        for item in items:
            info = item.find('a',class_='v-align-middle')
            # 获取资源描述信息
            name = item.find('p',class_='mb-1').text
            # 获取链接
            link = "https://github.com" + info['href']
            # 获取星标数
            stars = int(item.find('div',class_='mr-3').find('a',class_='Link--muted').text.strip())
            print(link+" "+str(stars))
            one = {
                "name" : name,
                "url" : link,
                "stars" : stars
            }
            self.list.append(one)

    def crawl_download_url(self):
        for index,item in enumerate(self.list):
            url = item["url"]
            # res = requests.get(url,headers=self.headers,proxies=proxies)
            res = requests.get(url,headers=self.headers)
            print(res.status_code)
            soup = BeautifulSoup(res.text,'html.parser')
            print(soup.text)
            a = soup.find_all('a',class_='d-flex flex-items-center color-fg-default text-bold no-underline')
            print(len(a))
            for x in a:
                print(x.text)
            downloadUrl = web_url + a[1]['href']
            self.list[index]['downloadUrl'] = downloadUrl
        return self.list

    def crawl(self):
        self.crawl_link()
        return self.crawl_download_url()



    
        

