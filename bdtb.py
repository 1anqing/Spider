'''
Created on 2018年7月13日

@author: li
'''
import requests
from bs4 import BeautifulSoup
import re
import os

class HtmlDownloader():
    
    def downloader(self, url):
        try:
            r = requests.get(url, timeout=30)
            r.encoding = 'utf-8'
            return r.text
        except Exception as e:
            print(str(e))
            return None
        
    def imgSave(self, url):
        try:
            r = requests.get(url, timeout=30)
            if not os.path.exists('imgs'):
                os.mkdir('imgs')
            path = 'imgs' + '//' + url.split('/')[-1]
            if not os.path.exists(path):
                with open(path, 'wb') as fp:
                    fp.write(r.content)
        except Exception as e:
            print(str(e))
        

class HtmlParser():
    
    def parser(self, response):
        page = BeautifulSoup(response, 'html.parser')
        pageNumber = page.find('span', {'class':'red_text'}).text
        count = int(int(pageNumber) / 50)
        for i in range(count + 1):
            yield i 
    
    def getLinks(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        url = 'https://tieba.baidu.com'
        aList = soup.find_all('a', {'rel':'noreferrer', 'href':re.compile('\/p\/[0-9]+')})
        href = [url + i['href'] for i in aList]
        return href
        
    
    def getImg(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        img = soup.find_all('img', {'class':'BDE_Image'})
        for i in img:
            yield i['src']
        
            
        
class Spider():
    
    def __init__(self, url):
        self.url = url
        self.parser = HtmlParser()
        self.downloader = HtmlDownloader()
        
        
    def getPages(self):
        response = self.downloader.downloader(self.url)
        urlList = [self.url[0:-1] + str(i * 50) for i in self.parser.parser(response)]    
        return urlList
    
       
    def getAllLinks(self):
        pageList = self.getPages()
        for i in pageList:
            response = self.downloader.downloader(i)
            href = self.parser.getLinks(response)
            yield href
             
            
    def saveImg(self):
        for i in self.getAllLinks():
            for j in i:
                response = self.downloader.downloader(j)
                img = self.parser.getImg(response)
                for k in img:
                    self.downloader.imgSave(k)

                    
    def run(self):
        pass
                      
        
if __name__ == '__main__':
    start_url = input('Please input the start url: ')
    spider = Spider(start_url)
    spider.saveImg()
        
        
        

