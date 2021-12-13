import argparse
import importlib
import openpyxl
import requests
import websites
import os
import zipfile
import time
from multiprocessing.dummy import Pool as ThreadPool # 并发下载
from fake_useragent import UserAgent
from websites.github import Spider

class Crawler:
    key = ""
    name = ""
    limit = 20
    language = ""
    star = 0
    save_path = r"C:\Users\JM\Desktop\pythonCodes\plantuml_crawler\OutputFiles"
    headers = {'User-Agent':str(UserAgent().random)}
    # proxies = {
    #     "http" : "101.32.251.31:10488",
    # }

    def __init__(self):

        # 执行代码所需的参数
        parser = argparse.ArgumentParser(description="必要和可选的参数信息")
        parser.add_argument('-k','--key')   # 搜索关键字
        parser.add_argument('-n','--name',default='github') # 搜索站点
        parser.add_argument('-l','--limit',default=20)  # 搜索条数
        parser.add_argument('-lang','--language')   # 相关语言
        parser.add_argument('-s','--star',default=0) # 星标限制
        args = parser.parse_args()
        self.key = args.key
        self.name = args.name
        self.limit = args.limit
        self.language = args.language
        self.star = args.star
        print("关键字：{}  站点：{}  语言：{}  条数：{} 星标：{}".format(self.key,self.name,self.language,self.limit,self.star))

        # 导入需要的爬虫模块
        module_name = "websites.{}".format(self.name)
        self.website = self.dynamic_import(module_name)
        

    # 动态导入所需模块
    def dynamic_import(self,module):
        return importlib.import_module(module)


    # 过滤筛选
    def filter(self):
        list = []
        for item in self.list:
            stars = item['stars']
            if stars >= self.star:
                list.append(item)
        self.list = list


    # 生成报表
    def reportForm(self):
        wb = openpyxl.Workbook()
        sheet = wb.active
        # 录入表头
        sheet.append(['项目名','项目链接','stars','下载地址'])
        # 录入数据
        for i in self.list:
            sheet.append(i)
        # 保存文件
        wb.save('reportForm.xlsx')
        

    # 单个的下载
    def download(self,contdict):
        name = contdict['name'].replace('\\','_')   # 文件名不能有“\”,故替换为“_”
        downloadUrl = contdict['downloadUrl']
        path = self.save_path
        # 如果路径不存在则创建路径
        if not os.path.exists(path):
            os.makedirs(path)
        # 下载文件
        # content = requests.get(downloadUrl,headers=self.headers,proxies=self.proxies).content
        content = requests.get(downloadUrl,headers=self.headers).content
        fileName = name + '.zip'
        with open(fileName,'wb') as f:
            f.write(content)
        print(name+'下载完成')
        # 解压文件
        zip_file = zipfile.ZipFile(fileName)
        zip_file.extract(zipfile,path)
        zip_file.close()
        print(name+'解压完成')


    # 多进程下载
    def download_start(self,list):
        start = time.time()
        pool = ThreadPool(4)

        result = pool.map(self.download,list)
        pool.close()
        pool.join()
        end = time.time()
        print('下载用时：'+str(end-start))


    # 开始爬取
    def crawl(self):
        # 得到链接列表
        w = self.website.Spider(self.key,self.language,self.limit)
        self.list = w.crawl()
        print(self.list)
        

if __name__ == '__main__':
    c = Crawler()
    # 爬取得到链接列表
    c.crawl()
    # 过滤筛选
    c.filter()
    # 并发下载解压
    c.download_start()

