# -*- coding:utf-8 -*-
import sys
import os
from selenium import webdriver
from requests import Session
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import weixin as WeixinCP
from time import sleep
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
'''
各软件跟包的版本信息
python:2.7.13
cx_Oracle:5.2.1
selenium:3.4.1
firefox:60.4.2
geckodriver:v0.21.0
'''
#企业号接收者对应的userid，多人可通过 '|' 连接
toUser = '熊游泳|庾玲'
req = Session()
req.headers.clear()
options = FirefoxOptions()
options.add_argument("--headless")
wd = webdriver.Firefox(firefox_options=options)
#IP PORT 为Enterprise Manager Cloud Control Console对应的IP跟端口
logInUrl = 'https://134.176.123.46:7802/em/faces/logon/core-uifwk-console-login'
wd.get(logInUrl)
#填写对应的登录账号跟密码，默认账号是sysman，password请替换为登录密码
wd.find_element_by_xpath('//*[@id="j_username::content"]').send_keys('sysman')
wd.find_element_by_xpath('//*[@id="j_password::content"]').send_keys('WeLove_911')
sleep(2)
wd.find_element_by_xpath('//*[@id="login"]').click()
sleep(2)
wd.find_element_by_xpath('//*[@id="emT:lrmd1:iCustVw:4:custViewLink"]').click()
sleep(2)
i = 1
wxPostList = []
# start with 0 column
while i < 100 :
    j = 1
    while j < 100 :
        # 只爬取了Target、Severity、Last Updated、Summary四个相对关键的字段的信息
        xPathColumn1 = '//*[@id="emT:lrmd1:tbmd1:pc2:t2::db"]/table[' + str(i) + ']/tbody/tr[' + str(j) + ']/td[2]/div/table/tbody/tr/td[1]'
        xPathColumn2 = '//*[@id="emT:lrmd1:tbmd1:pc2:t2::db"]/table[' + str(i) + ']/tbody/tr[' + str(j) + ']/td[2]/div/table/tbody/tr/td[2]'
        xPathColumn3 = '//*[@id="emT:lrmd1:tbmd1:pc2:t2::db"]/table[' + str(i) + ']/tbody/tr[' + str(j) + ']/td[2]/div/table/tbody/tr/td[3]'
        xPathColumn6 = '//*[@id="emT:lrmd1:tbmd1:pc2:t2::db"]/table[' + str(i) + ']/tbody/tr[' + str(j) + ']/td[2]/div/table/tbody/tr/td[6]'
        try :
            tableElementColumn1 = wd.find_element_by_xpath(xPathColumn1)
            tableElementColumn2 = wd.find_element_by_xpath(xPathColumn2)
            tableElementColumn3 = wd.find_element_by_xpath(xPathColumn3)
            tableElementColumn6 = wd.find_element_by_xpath(xPathColumn6)
            tableElementColumn1ImgTag = tableElementColumn1.find_element_by_tag_name("img")
            tableElementColumn1Content = tableElementColumn1ImgTag.get_attribute("title")
            tableElementColumn2Content = tableElementColumn2.get_attribute('textContent')
            tableElementColumn3Content = tableElementColumn3.get_attribute('textContent')
            tableElementColumn6Content = tableElementColumn6.get_attribute('textContent')
            tempMsg = \
                "Target: " + tableElementColumn3Content +  "\n" \
                + "Severity: " + tableElementColumn1Content + "\n" \
                + "Last Updated: \n" + tableElementColumn6Content[0:24]  + "\n" \
                + "Summary: " + tableElementColumn2Content + "\n\n"
            wxPostList.append(tempMsg)
            j = j + 1
        except :
            break
    i = i  + 1
wd.quit()

i = 0
j = 0
wxMsg = '**公司\n**机房数据库巡检结果：\n\n'
#每10条告警信息推送一条企业号文本信息
if len(wxPostList) > 0 :
    for i in range(len(wxPostList)) :
        wxMsg = wxMsg + wxPostList[i]
        #避免信息超过企业号信息允许的最大长度，每10条告警信息推送一次
        if j == 9 or i ==  (len(wxPostList) - 1):
            #需要将信息转换成utf-8格式
            wxMsg = wxMsg.encode('utf-8')
            weixinCP = WeixinCP.Weixin()
            weixinCP.get_token()
            msg = weixinCP.send_data(toUser, wxMsg)
            wxMsg = ''
            j = 0
        j = j + 1
else:
    wxMsg = wxMsg +  '所有**机房数据库无任何告警信息！'
    weixinCP = WeixinCP.Weixin()
    weixinCP.get_token()
    msg = weixinCP.send_data(toUser, wxMsg)