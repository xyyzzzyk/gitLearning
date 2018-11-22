#!/usr/local/python27/bin/python3.7

import xlrd
import paramiko
import logging
import requests

# init log module
logger = logging.getLogger('connect')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('weak_pwd_test.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

#open excel
def open_excel(files):
    try:
        data = xlrd.open_workbook(files)
        return data
    except Exception as e:
        print(str(e))

def ssh_connect(host,user,pwd):
    flag = 0
    try:
        s = paramiko.SSHClient()
        paramiko.util.log_to_file('paramiko.log')
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # logger.info(host + "  with passwd: " + pwd.center(20) +"len:   "+str(len(pwd)).center(10) )
        s.connect(
                hostname=host,
                port=22,
                username=user,
                password=pwd,
                timeout=5,
                allow_agent=False,
                look_for_keys=False)
    except Exception as e:
                logger.error(host + user.center(10) + "  with passwd: " + pwd.center(15) +"len:   "+str(len(pwd)).center(5) + str(e))
                flag = 1  
    except paramiko.ssh_exception.AuthenticationException:
                logger.error("host:" + host + "  with passwd: " + pwd + " not match")
                flag = 0
    except paramiko.ssh_exception.SSHException:
                logger.error("host:" + host + " SSH connect fail   /"+str(e))
                flag = 0

    
    s.close()
    return flag

def connectHost(excelFile, a_col, b_col, c_col):
    data = open_excel(excelFile)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    vflag = 0
    for rdata in range(nrows):
        vhost = str(table.cell(rdata, a_col).value)
        vuser = str(table.cell(rdata, b_col).value)
        vpwd = str(table.cell(rdata, c_col).value)
        vflag = vflag + ssh_connect(vhost,vuser,vpwd)

    logger.info("Total Error :" + str(vflag))

def main(xFile):
    host_col = 6
    begin_row = 0
    pwd_col = 0
    connectHost(xFile, 0, 1, 2)

if __name__ == "__main__":
    xlsFile = "weakpwd.xlsx"
    main(xlsFile)
