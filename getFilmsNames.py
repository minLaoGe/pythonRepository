# grab web page by multiple thread

import  os
import requests
#导入 etree类
from lxml import etree
import threading
from concurrent.futures import ThreadPoolExecutor


types = set()
timeout=30
baseUrl = ''
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"}

def getH2Childs(url,file):
    filmsUrl = url.attrib.get('href')
    filmsName = url.tail
    file.write(" name: " + filmsName +"\n")
    downUrl = baseUrl + filmsUrl
    print("begin work-----")
    try:
        saveMovieInfoMation(downUrl,file)
    except BaseException as e:
        print("have probelm")
        print(e)
    else:
        print("finish")
    print("over get Childs -----")
    # saveFiles(downUrl)




# def saveFiles(url):
#     page = requests.get(url)
#     file = open('page'+ str(random.randint(0,100000)) +".html","w")
#     file.write(page.text)
#     file.close()

def saveMovieInfoMation(url,file):
    page = requests.get(url,timeout=timeout)
    filesDom = etree.HTML(page.text)
    doms = filesDom.xpath('//div[@class="content"]//ul[@class="seeds"]//li//*')
    for ele in doms:
        if 'code' == ele.tag  and str(ele.text).find('GB')>=0:
            size = ele.text
            file.write(" \t\t  大小: "+size +"\n")
            print(size)
        elif  'a' == ele.tag:
            att = ele.attrib
            downUrl = baseUrl + att.get('href' )
            title =  att.get('title')
            file.write("\t\t链接: " + downUrl+"\n")
            file.write("\t\t名称: "+title+"\n")
            print(downUrl)
            print(title)



def getUrls(ele):
    filmsUrl = ele.attrib.get('href')
    downUrl = baseUrl + filmsUrl
    return downUrl;

def getCusiveUrls(url,file):
    print("Task 1 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 1: {}".format(os.getpid()))
    req = requests.get(url,timeout=timeout)
    #获取列表
    text = etree.HTML(req.text)
    pages=text.xpath('//div[@class="page-nav"]//span[last()-1]//a/text()')
    # print("pages: [ "+type(pages[0])+' ]')
    print(pages[0])
    pageNum = int(pages[0])
    while pageNum > 0:
        req = requests.get(url + "?page=" +str(pageNum), timeout=timeout)
        htmlText = req.text;
        # 获取列表
        text = etree.HTML(htmlText)
        subPage = text.xpath('//div[@class="content"]//h2//*')
        for i in subPage:
            # pool2.submit(getH2Childs,i, file)
            getH2Childs(i, file)
        pageNum = pageNum -1
    file.close()

if __name__ == '__main__':


    dom=etree.parse("./filesms.html",etree.HTMLParser())
    # print(textwrapper)
    # dom = etree.HTML(textwrapper)
    a_text = dom.xpath('//div[@class="sidebar"]//li[@class="sidebar-sub-header"]//a')

    pool = ThreadPoolExecutor(max_workers=5)
    i = 0.01
    # tabside
    for item in a_text:
        type = item.text
        file = open(type+".txt", 'a')
        downUrl = getUrls(item)
        pool.submit(getCusiveUrls,downUrl,file)
