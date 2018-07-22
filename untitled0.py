# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 20:38:09 2018

@author: 16597
"""
import jieba
import pandas as pd
from collections import Counter
import re
from string import punctuation 
from functools import reduce
import numpy as np
add_punc='，。、【】“”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=擅长于的&#@￥'
all_punc=punctuation+add_punc
def sortTwo(inputStr):
    inputArr = inputStr.split(",")
    result = ""
    if(int(inputArr[0]) > int(inputArr[1])):
        result = inputArr[1] + "," + inputArr[0]
    else:
        result = inputArr[0] + "," + inputArr[1]
    return result
def sentence_cut(x):#cut words and delete punctuation
    testline = jieba.cut(x,cut_all=False)
    testline=' '.join(testline)
    testline=testline.split(' ')
    te2=[]
    for i in testline:
        te2.append(i)
        if i in all_punc:
            te2.remove(i)
    return set(te2)
def splitWord(inputSen):
    inputSen = sentence_cut(inputSen)
    return ",".join(inputSen)
# 在默认模式下有对中文歧义有较好的分类方式
#打开文件
f = open('D:\proj\weibo.top10wan', encoding='utf-8')                  
result = {}
#读取文件内容到字典
for line in f.readlines():
    inner = {}
    r = line.split("\t")
    inner["crawler_time"] = r[1]
    inner["crawler_time_stamp"] = r[2]
    inner["is_retweet"] = r[3]
    inner["user_id"] = r[4]
    inner["nick_name"] = r[5]
    inner["tou_xiang"] = r[6]
    inner["user_type"] = r[7]
    inner["weibo_id"] = r[8]
    inner["weibo_content"] = r[9]
    inner["zhuan"] = r[10]
    inner["ping"] = r[11]
    inner["zhan"] = r[12]
    inner["url"] = r[13]
    inner["device"] = r[14]
    inner["locate"] = r[15]
    inner["time"] = r[16]
    inner["time_stamp"] = r[17]
    inner["r_user_id"] = r[18]
    inner["r_nick_name"] = r[19]
    inner["r_user_type"] = r[20]
    inner["r_weibo_id"] = r[21]
    inner["r_weibo_content"] = r[22]
    inner["r_zhuan"] = r[23]
    inner["r_ping"] = r[24]
    inner["r_zhan"] = r[25]
    inner["r_url"] = r[26]
    inner["r_device"] = r[27]
    inner["r_location"] = r[28]
    inner["r_time"] = r[29]
    inner["r_time_stamp"] = r[30]
    inner["pic_content"] = r[31]
    result[line.split()[0]] = inner
f.close()
#创建dataframe
d = pd.DataFrame(result).T
#统计一天微博数据总量 100000
print(d["user_id"].count())
#统计一天微博发文user_id总量 47661
print(d["user_id"].value_counts().count())
#统计一天微博发文weibo_id总量  96688
print(d["weibo_id"].value_counts().count())
#统计一天微博发文最多的top 100个用户
v = d["weibo_id"]
print (Counter(v).most_common(1))
#统计一天微博转发最多的设备类型和最少的设备类型
v = d["r_device"]
print (Counter(v).most_common(1))
#找出特定的weiboid
#对每条微博的内容进行分词
c = (d.loc[d['user_id'].str.contains('1638782947')])["weibo_content"].map(lambda x:splitWord(x))
#r = reduce(lambda x,y:x+y, c)
#print(r)
word_lst = []
word_dict= {} 
for word in c: 
    word_lst.append(word.split(','))  
    for item in word_lst: 
        for item2 in item: 
            if item2 not in word_dict: 
                word_dict[item2] = 1
            else: 
                word_dict[item2] += 1
print(sorted(word_dict.items(),key = lambda x:x[1],reverse = True)[:5])
#计算微博数据中的好基友，找到相互转发数量最大的基友pair，按照相互转发量排序
#1.先选取出这三列,去重，统计基友
pair = d[["user_id","r_user_id","weibo_id"]]
pair1 = pair.drop_duplicates(subset=["user_id","r_user_id","weibo_id"],keep='first')
#print(pair1)
#2统计A,B B,A的对数
gp=pair1.groupby(by=["user_id","r_user_id"])
newdf=gp.size()
countnum = newdf.reset_index(name='times')
countnum.drop((countnum["r_user_id"][countnum["r_user_id"] == ""]).index.tolist(),inplace = True)
countnum.drop((countnum[(countnum["user_id"] == countnum["r_user_id"])]).index.tolist(),inplace = True)
#3输出结果
countnum["newcount"] = countnum.apply(lambda x:x["user_id"]+','+x["r_user_id"], axis = 1)
countnum["tmp"] = countnum["newcount"].map(lambda x:sortTwo(x))
#print(countnum)
gp1 = countnum["times"].groupby(countnum["tmp"])
countpair = gp1.min().sort_values(ascending=False)
#输出前十个
print(countpair[:10])

