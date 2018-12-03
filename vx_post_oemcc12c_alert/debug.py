from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# browser = webdriver.Firefox()
# browser.get('http://www.baidu.com/')


# options = FirefoxOptions()
# options.add_argument("--headless")
# wd = webdriver.Firefox(options=options)
wd = webdriver.Firefox()
#IP PORT 为Enterprise Manager Cloud Control Console对应的IP跟端口
logInUrl = 'https://134.176.123.46:7802/em/faces/logon/core-uifwk-console-login'
wd.get(logInUrl)

wd.find_element_by_xpath('//*[@id="j_username::content"]').send_keys('sysman')
wd.find_element_by_xpath('//*[@id="j_password::content"]').send_keys('WeLove_911')
sleep(2)
wd.find_element_by_xpath('//*[@id="login"]').click()
sleep(2)
wd.find_element_by_xpath('//*[@id="emT:lrmd1:iCustVw:4:custViewLink"]').click()
sleep(2)
i = 1
wxPostList = []