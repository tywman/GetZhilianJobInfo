# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 12:29:11 2017

@author: Administrator
"""
from lxml import etree
import re

job_desc_list = ['职位名称','职位链接','工作地点','职位月薪','公司名称','工作经验',\
                 '工作性质','发布日期','最低学历','招聘人数','职位类别','职位描述']
                   
company_desc_list=['公司名称','公司链接','公司福利','公司介绍','公司规模',\
                   '公司性质','公司行业','公司主页','公司地址','关键词']

class JOB(object):
    jobs = {}
    jobsTitles = ['zwmc','zwlj','gzdd','zwyx','gsmc','gzdd','gzjy',\
                  'gzxz','fbrq','zdxl','zprs','zwlb','zwms']
    company = {}
    companyTitles = ['gsmc','gslj','gsfl','gsjs','gsgm',\
                     'gsxz','gshy','gszy','gsdz','gjc']
    title_desc = {}
    def __init__(self):
        self.clearJob()
        self.clearCompany()

    def clearJob(self):
        for jobTitle in self.jobsTitles:
            self.jobs[jobTitle] = ''
        return self.jobs
    
    def clearCompany(self):
        for companyTitle in self.companyTitles:
            self.company[companyTitle] = ''
        return self.company
        
    def list2dic(self,itemlist):
        if len(itemlist) == len(self.titles):
            for num in range(len(self.titles)):
                self.job[self.titles[num]] = itemlist[num]
            return self.job
        else:
            return self.dicclear()
    '''获取职位表头信息'''
    def get_Job_desc(self,index):
        if (index < len(self.job_desc_list)) and (index >= 0):
            return job_desc_list[index]
        else:
            return '输入索引错误'
    '''获取公司表头信息'''
    def get_Company_desc(self,index):
        if (index < len(self.company_desc_list)) and (index >= 0):
            return company_desc_list[index]
        else:
            return '输入索引错误'
        
class JOBExplain(JOB):
    JobDetail = {}
    def __init__(self):
        JOB.__init__(self)
        
    def JobExplor(self,html,flag):
        response = etree.HTML(html)
        if flag:
            for i in response.xpath('//div[@class="inner-left fl"]'):
                job_name = i.xpath('h1/text()')                     # 职位名称
                company_name = i.xpath('h2/a/text()')               # 公司名称
                company_link = i.xpath('h2/a/@href')                # 公司链接
                job_advantage = ','.join(i.xpath('div[1]/span/text()')) # 公司福利
            for i in response.xpath('//ul[@class="terminal-ul clearfix"]'):
                job_salary = i.xpath('li[1]/strong/text()')             # 职位月薪
                job_place = i.xpath('li[2]/strong/a/text()')            # 工作地点
                job_post = i.xpath('li[3]//span[@id="span4freshdate"]/text()')  # 发布日期
                job_nature = i.xpath('li[4]/strong/text()')         # 工作性质
                job_experience = i.xpath('li[5]/strong/text()')     # 工作经验
                job_education = i.xpath('li[6]/strong/text()')      # 最低学历
                job_number = i.xpath('li[7]/strong/text()')         # 招聘人数
                job_kind = i.xpath('li[8]/strong/a/text()')         # 职位类别

    #        html_body=html
            reg = r'<!-- SWSStringCutStart -->(.*?)<!-- SWSStringCutEnd -->'
            reg = re.compile(reg, re.S)
            content = re.findall(reg, html)
            try:
                content = content[0].strip()  # strip去空白
                reg_1 = re.compile(r'<[^>]+>')  # 去除html标签
                content = reg_1.sub('', content).replace('&nbsp', '')
                job_content= content                                # 职位描述
            except Exception as e:
                job_content=''
    
            for i in response.xpath('//div[@class="tab-inner-cont"]')[0:1]:
                job_place = i.xpath('h2/text()')[0].strip()         #工作地点（具体）
    
            for i in response.xpath('//div[@class="tab-inner-cont"]')[1:2]:
                reg = re.compile(r'<[^>]+>')
                company_content = reg.sub('',i.xpath('string(.)')).replace('&nbsp', '')  # 公司介绍
                company_info = company_content
    
            for i in response.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]'):
                if u'公司主页' in i.xpath('string(.)'):
                    company_size = i.xpath('li[1]/strong/text()')           # 公司规模
                    company_nature =i.xpath('li[2]/strong/text()')          
                    company_industry = i.xpath('li[3]/strong/a/text()')     # 公司行业
                    company_home_link = i.xpath('li[4]/strong/a/text()')    # 公司主页
                    company_place = i.xpath('li[5]/strong/text()')          # 公司地址
                else:
                    company_size = i.xpath('li[1]/strong/text()')
                    company_nature = i.xpath('li[2]/strong/text()')
                    company_industry = i.xpath('li[3]/strong/a/text()')
                    company_home_link = [u'无公司主页']
                    company_place = i.xpath('li[4]/strong/text()')
            
            JOB.jobs['zwmc'] = str(job_name[0])
            JOB.jobs['zwlj'] = str(company_link[0])
            JOB.jobs['gzdd'] = str(job_place[0])
            JOB.jobs['zwyx'] = str(job_salary[0])
            JOB.jobs['gsmc'] = str(company_name[0])
            JOB.jobs['gzjy'] = str(job_experience[0])
            JOB.jobs['gzxz'] = str(job_nature[0])
            JOB.jobs['fbrq'] = str(job_post[0])
            JOB.jobs['zdxl'] = str(job_education[0])
            JOB.jobs['zprs'] = str(job_number[0])
            JOB.jobs['zwlb'] = str(job_kind[0])
            JOB.jobs['zwms'] = str(job_content)
            
            JOB.company['gsmc'] = str(company_name[0])
            JOB.company['gslj'] = str(company_link[0])
            JOB.company['gsfl'] = str(job_advantage)
            JOB.company['gsjs'] = str(company_info)
            JOB.company['gsgm'] = str(company_size[0])
            JOB.company['gsxz'] = str(company_nature[0])
            JOB.company['gshy'] = str(company_industry[0])
            JOB.company['gszy'] = str(company_home_link[0])
            JOB.company['gsdz'] = str(company_place[0].strip())
            JOB.company['gjc'] = str(job_name[0])
            
            return JOB.jobs,JOB.company
        else:
            return JOB.clearJob(),JOB.clearCompany()
        