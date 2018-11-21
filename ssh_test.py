#!/usr/local/python27/bin/python3.7

import xlrd
import paramiko
import logging
import requests

# init log module
logger = logging.getLogger('connect')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('exec.log')
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

def ssh_connect(host,pwd):
    flag = 1
    try:
        s = paramiko.SSHClient()
        paramiko.util.log_to_file('paramiko.log')
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        s.connect(
                hostname=host,
                port=22,
                username='ampmon',
                password=pwd,
                timeout=2)
    
    except paramiko.ssh_exception.AuthenticationException:
                logger.error("host:" + host + "  with passwd: " + pwd + " not match")
                flag = 0
    except paramiko.ssh_exception.SSHException:
                logger.error("host:" + host + " SSH connect fail   /"+str(e))
                flag = 0
    except Exception as e:
                logger.error(host + "  with passwd: " + pwd.center(20) +"len:   "+str(len(pwd)).center(10) + str(e))
                flag = 0  
    
    s.close()
    return flag

def connectHost(excelFile, b_row, b_col, c_col):
    data = open_excel(excelFile)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    for rdata in range(nrows):
        vhost = str(table.cell(rdata,b_col).value)
        vpwd = str(table.cell(rdata, c_col).value)
        vflag=ssh_connect(vhost,vpwd)

"""         if vflag == 0 :
            break """

def main(xFile):
    host_col = 6
    begin_row = 0
    pwd_col = 0
    connectHost(xFile, 0, 6, 8)

if __name__ == "__main__":
    xlsFile = "xyy.xlsx"
    main(xlsFile)