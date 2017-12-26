# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 11:39:22 2017

@author: Administrator
"""

import xlwt#用来创建excel文档并写入数据

class FileOperate:
    workbook = ''
#    data_sheet = ''
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf-8') #注意这里的Workbook首字母是大写，无语吧
        
    def create_sheet(self, sheet_name):
        #创建sheet
        data_sheet = self.workbook.add_sheet(sheet_name,False)
        return data_sheet
    
    def write_row_file(self,data_sheet,items,row=0,col=0):
        #爬取到的内容写入excel表格
        for i in range(len(items)):
            data_sheet.write(row, col+i, items[i])
            
    def write_col_file(self,data_sheet,items,row=0,col=0):
        #爬取到的内容写入excel表格
        for i in range(len(items)):
            data_sheet.write(row+i, col, items[i])
#            print('row:%s,col:%s'%(row+i,col))
            
    def write_col_link_file(self,data_sheet,items,items_link,row=0,col=0):
        #爬取到的内容写入excel表格
        for i in range(len(items)):
            item = items[i]
            item = item.replace('\"','-')
            item_link = items_link[i]
            data_sheet.write(row+i, col, xlwt.Formula('HYPERLINK("%s";"%s")'%(item_link,item)))

    def save_file(self, file_name):
        self.workbook.save(file_name)

    def link_style(self,color):
        style = xlwt.XFStyle()   #初始化样式
        font = xlwt.Font()       #为样式创建字体
        font.name = 'Verdana'
        font.bold = False
        font.colour_index = 0
        font.height = 220
        style.font = font
        return style
    
    def content_style(name, height, bold = False):
        style = xlwt.XFStyle()   #初始化样式
        font = xlwt.Font()       #为样式创建字体
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style
    
    def title_style(self):
        style = xlwt.XFStyle()   #初始化样式
        font = xlwt.Font()       #为样式创建字体
        font.name = 'Verdana'
        font.bold = True
        font.colour_index = 0
        font.height = 220
        style.font = font

        return style