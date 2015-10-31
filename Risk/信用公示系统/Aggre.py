__author__ = 'Han'
#coding=utf-8
import os
from datetime import date
from YCParser import YCParser


def dealdate(cdate):
    k1=cdate.find('年')
    k3=len(cdate)
    year=int(cdate[0:4])
    if k1!=-1:
        k2=cdate.find('月')
        month=int(cdate[k1+1:k2])
        day=int(cdate[k2+1:k3-1])
    else:
        k1=cdate.find('-')
        if k1!=-1:
            k2=cdate[5:].find('-')+5
            month=int(cdate[5:k2])
            day=int(cdate[k2+1:k3])
        else:
            print(cdate+'\n')
            year=input('year=')
            month=input('month=')
            day=input('day=')
    return date(year,month,day)

if __name__=='__main__':
    yc=YCParser()
    rs='D:/GSXT/GSXTresult/'
    dirlist=os.listdir(rs)
    frecord=open('D:/GSXT/GSXT整理temp.txt','w')
    total=0
    ntotal=0
    idlist={}
    for dirr in dirlist:
        f=open(rs+dirr,'r')
        k=dirr.find('.')
        prov=dirr[:k]   #取省份
        recordlist={}   #记录字典
        yclist={}
        for line in f.readlines():
            total+=1
            if total % 10000==0:print(total)
            line=line.replace('\n','')
            infolist=line.split('|')
            if yc.checkname(infolist[0])==False: continue
            cdate=dealdate(infolist[4])      #时间类型
            infolist[4]=str(cdate)
            id=infolist[1]
            reason=infolist[3]
            infolist[-1]=prov
            if (infolist[5]!='') or (infolist[6]!=''):
                if id in yclist:
                    if reason in yclist[id]:yclist[id][reason]=max(cdate,yclist[id][reason])
                    else:yclist[id][reason]=cdate
                else:
                    yclist[id]={}
                    yclist[id][reason]=cdate
            else:
                if id not in recordlist:
                    recordlist[id]={}
                    recordlist[id][reason]=dict(date=cdate,write=infolist)
                else:
                    if (reason not in recordlist[id]) \
                            or (reason in recordlist[id]
                                and cdate>recordlist[id][reason]['date']):    #保留最新的记录
                        recordlist[id][reason]=dict(date=cdate,write=infolist)
                    else:continue
        for key in recordlist.keys():
            for reason in recordlist[key].keys():
                if not ((key in yclist) and (reason in yclist[key]) and (recordlist[key][reason]['date']<=yclist[key][reason])):
                    ilist=recordlist[key][reason]['write']
                    frecord.write('|'.join(ilist)+'\n')
                    ntotal+=1
                    if key not in idlist:idlist[key]=0
        f.close()
    frecord.close()
    print('total=',ntotal)
    print('compnum=',len(idlist))