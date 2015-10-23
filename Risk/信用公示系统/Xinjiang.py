__author__ = 'Chen'
#coding=utf-8
#日期顺序有问题
import urllib.parse,urllib.request

import re
from datetime import *
import time
from YCParser import YCParser

class GetYCParser(YCParser):

    def getinfopostdata(self,pri):
        postdata=urllib.parse.urlencode({
            'method':'jyycInfo',
            'maent.pripid':pri,
            'czmk':'czmk6',
            'random':str(time.time()*1000)
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            pageNos+=1
            url='http://gsxt.xjaic.gov.cn:7001/xxcx.do?method=ycmlIndex&random=10000000&cxyzm=no&entnameold=&djjg=&' \
                'maent.entname=&page.currentPageNo='+str(pageNos)+'&yzm='
            result=self.gethtml(url)
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            print('Page %d Reading' % pageNos)
            Namelist=result.findAll('li',attrs={'class':'tb-a1'})
            regIDlist=result.findAll('li',attrs={'class':'tb-a2'})
            datelist=result.findAll('li',attrs={'class':'tb-a3'})
            del Namelist[0]
            del regIDlist[0]
            del datelist[0]
            l=len(datelist)
            br=0
            for i in range(l):
                cdate=str(datelist[i].contents[0])
                reg=r'年(.*?)月'
                pattern=re.compile(reg)
                month=int(pattern.findall(cdate)[0])
                reg=r'月(.*?)日'
                pattern=re.compile(reg)
                day=int(pattern.findall(cdate)[0])
                cdate=date(int(cdate[0:4]),month,day)
                if cdate<startdate:
                    br=1
                    break
                else:
                    if cdate<=enddate:
                        priName=Namelist[i].find('a')
                        Name=priName.contents[0]
                        reg=r'doOpen\(\'(.*?)\'\)'
                        pattern=re.compile(reg)
                        pri=pattern.findall(str(priName))[0]
                        regID=regIDlist[i].contents[0]
                        entdict=dict(Name=Name,regID=regID,Date=cdate,pri=pri)
                        self.PrintInfo(entdict)
            if br==1:break

    def PrintInfo(self,ent):
        req=urllib.request.Request(
            url='http://gsxt.xjaic.gov.cn:7001/ztxy.do',
            data=self.getinfopostdata(ent.get('pri')),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=inforesult.find('tr',attrs={'name':'yc'}).findAll('td')
            self.gendown(ent,infolist)

if __name__=='__main__':
    location='新疆'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,9,23),enddate=date.today()-timedelta(days=0))



