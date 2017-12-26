# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 21:44:27 2017

@author: Administrator
"""

import urllib
import math,re
from lxml import etree
import sys
import importlib

importlib.reload(sys)

header={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

release_days = ['不限','今天','最近3天','最近1周','最近1月']

def get_html(url):
    req = urllib.request.Request(url, headers= header)
    resp = urllib.request.urlopen(req)
    html = resp.read().decode('utf-8')
    return html

'''
    得到不同城市的起始链接
    return:列表，包含不同城市的起始url，比如：
    http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&人工智能
'''
def get_start_url(job_list, place_list,release_day='不限'):
    # 先主要爬主要城市，看不同需求，也可以爬全国，只要把智联的候选地点全部抓取下来即可
    rel = r''
    if(release_day == '不限'):
        rel = r'&pd=-1'
    elif(release_day == '今天'):
        rel = r'&pd=1'
    elif(release_day == '最近3天'):
        rel = r'&pd=3'
    elif(release_day == '最近1周'):
        rel = r'&pd=7'
    elif(release_day == '最近1月'):
        rel = r'&pd=30'
    else:
        rel = r'&pd=-1'
        
    total_urls = []
    for keyword in job_list:
        list_urls = []
        for place in place_list:
            url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=' + urllib.parse.quote(str(place)) + '&kw=' + urllib.parse.quote(keyword) + rel
#            url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=' + str(place) + '&kw=' + keyword
            list_urls.append(url)
        total_urls.append((keyword, list_urls))
    return total_urls


def get_page(url):
    '''得到每个区的页数'''
    html = get_html(url)
    reg = r'共<em>(.*?)</em>个职位满足条件'
    reg = re.compile(reg)
    job_count = int(re.findall(reg, html)[0])
    job_count_page = math.ceil(job_count / 60)
    return job_count_page

'''从页面获取职位信息'''
def get_job_from_page(html):
    response = etree.HTML(html)
    job_names = []
    return_ratio = []
    job_link = []
    company_name = []
    '''取得职位名称'''
    for table in response.xpath('//td[@class="zwmc"]'):
        table = table.xpath('div/a[1]')
        for i in table:
            '''取得职位链接'''
            job_link.append(i.xpath('@href')[0])
            reg = re.compile(r'<[^>]+>')
            job_content = reg.sub('',i.xpath('string(.)')).replace('&nbsp', '')
            job_names.append(job_content)
            
    for table in response.xpath('//div[@class="newlist_list_content"]'):
        return_ratio.append(table.xpath('table[2]/tr/td[2]/span/text()'))
        
    '''取得公司名称'''
    for table in response.xpath('//td[@class="gsmc"]'):
        table = table.xpath('a[1]')
        for i in table:
            reg = re.compile(r'<[^>]+>')
            company_content = reg.sub('',i.xpath('string(.)')).replace('&nbsp', '')
            company_name.append(company_content)
            
    money = response.xpath('//td[@class="zwyx"]/text()')
    position = response.xpath('//td[@class="gzdd"]/text()')
    
    job_info = {'job_name':job_names,'job_link':job_link,'return_ratio':return_ratio,'company_name':company_name,'money':money,'position':position}
    return job_info

'''从页面获取职位信息'''
def get_next_page(html):
    response = etree.HTML(html)
    next_page_link = response.xpath('//li[@class="pagesDown-pos"]/a[@class="next-page"]/@href')
    return next_page_link


'''从页面获取职位信息'''
def get_current_page(html):
    response = etree.HTML(html)
    current_page = response.xpath('//li/a[@class="current"]/text()')
    if current_page:
        return current_page[0]
    else:
        return '1'

def get_low_high_from_money(moneys):
    lows = []
    highs = []
    for money in moneys:
        if(money.find('-')>0):
            low = float(money[:money.find('-')])
            high = float(money[money.find('-')+1:])
        else:
            low = 0
            high = 0
        lows.append(low)
        highs.append(high)
    return lows,highs