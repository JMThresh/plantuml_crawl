class Spider:
    def __init__(self,key,limit):
        self.key = key
        self.limit = limit
        print("this is gitee's Spider:{},{}".format(key,limit))
    def crawl_link(self):
        list = {'gitee':'gitee','b':'def'}
        return list


    def crawl(self):
        self.crawl_link()
        return self.crawl_download_url()
