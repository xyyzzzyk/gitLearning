# -*- coding: utf-8 -*-
import urllib
import json
import cx_Oracle
'''
有注释的地方需要修改成与本人具体情况一致的，共计5处
'''
class Weixin(object):
    def __init__(self):
        #企业号corp_id
        self.corp_id = 'wwd62fb0daa14feb17'
        #应用所在组对应的secret
        self.corp_secret = '-Kx-sg3OG-JbYFY-UUALJnY6s5vZKndt6nRLl97V5HU'
        self.baseurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(self.corp_id, self.corp_secret)
        self.send_values = {}

    def get_token(self):
        #填写连接数据库   账号 密码ip port instance_name
        conn = cx_Oracle.connect('****/****@ip:port/instance_name')
        cur = conn.cursor()
        #企业号ACCESS_TOKEN通过python脚本定时爬取存在了WX_ACCESS_TOKEN表
        sql = "select * from WX_ACCESS_TOKEN"
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            self.access_token = row[0]
        cur.close()
        conn.close()
        return self.access_token

    # Send Message
    def send_data(self, userid, message):
        self.message = message
        self.send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        self.send_values = {
            "touser": userid,
            "msgtype": "text",
            #企业号内应用对应的agentid，本人的是55
            "agentid": "1000002",
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_data = json.dumps(self.send_values, ensure_ascii=False)
        send_request = urllib.Request(self.send_url, send_data)
        response = urllib.urlopen(send_request)
        msg = response.read()
        print(userid + ':' + msg)
        return msg