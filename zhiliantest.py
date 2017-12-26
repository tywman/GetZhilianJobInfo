# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 13:34:24 2017

@author: Administrator
"""

from zhilian_job_detail import JOBExplain
import datetime
import zhilian_urlFunction as urlFunc
from zhilian_FileFunc import FileOperate as FO

#    place_name = ['北京','上海', '广州', '深圳', '天津', '武汉', '西安', '成都', '大连', '长春', '沈阳', '南京', '济南', '青岛',
#                   '杭州', '苏州', '无锡', '宁波', '重庆', '郑州', '长沙', '福州', '厦门', '哈尔滨', '石家庄', '合肥', '惠州']
#    job_name = ['数据分析', 'php', '大数据', 'java', 'UI', 'IOS', '安卓', 'C++', 'python', '前端', '.net', '测试', '产品经理', '网络营销',
#                '嵌入式', '项目经理', 'VR', 'AR']
place_list = ['深圳']
job_list = ['数据分析','python','产品经理','项目经理','人工智能','总经理','图像','视觉','技术总监','技术负责人','人脸识别']
release_day = '今天'
#job_list = ['人工智能']

file = FO()

urls = urlFunc.get_start_url(job_list,place_list,release_day)
print(urls)
#urls = [('技术负责人', ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E6%8A%80%E6%9C%AF%E8%B4%9F%E8%B4%A3%E4%BA%BA&pd=1'])]

for tp in urls:
    keyword = tp[0]
    start_urls = tp[1]
#    start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E6%8A%80%E6%9C%AF%E8%B4%9F%E8%B4%A3%E4%BA%BA&pd=1']
    data_sheet = file.create_sheet(keyword)
    count = 1
    file.write_row_file(data_sheet,['职位名称','公司名称','职位月薪','工作地点'],0,0)
    for start_url in start_urls:
        print('起始页：' + start_url)
        while(True):
            # 从页面获取简单职位信息
            html = urlFunc.get_html(start_url)
            print(keyword + '---当前页面：' + urlFunc.get_current_page(html))
            jobs = urlFunc.get_job_from_page(html)
            low,high = urlFunc.get_low_high_from_money(jobs['money'])
            
            file.write_col_link_file(data_sheet,jobs['job_name'],jobs['job_link'],count,0)
            file.write_col_file(data_sheet,jobs['company_name'],count,1)
            file.write_col_file(data_sheet,jobs['money'],count,2)
            file.write_col_file(data_sheet,jobs['position'],count,3)
            file.write_col_file(data_sheet,low,count,4)
            file.write_col_file(data_sheet,high,count,5)
            count += len(jobs['job_name'])
#            print(jobs)
            # 获取下一页网页链接
            next_page_link = urlFunc.get_next_page(html)
            if(len(next_page_link) == 0):
                break
            else:
                start_url = next_page_link[0]

now = datetime.datetime.now()
title = now.strftime('%Y-%m-%d-%H-%M') 
file.save_file('智联-'+ title + '-搜索-' + release_day + '.xls')
        


#testlist = ['数据分析专员', 'http://jobs.zhaopin.com/440610485250159.htm', '深圳市万通顺达科技股份有限公司 ']
#html = urlFunc.get_html('http://jobs.zhaopin.com/582142423250746.htm')
#
#        
#        
#Info = JOBExplain()
#job,company = Info.JobExplor(html,True)
#print(job)
#print(company)
#
#jobdetail = job.list2dic(testlist)
#print(jobdetail)
#
#testlist2 = [' ',' ',' ']
#jobdetail2 = job.list2dic(testlist2)
#print(jobdetail2)
