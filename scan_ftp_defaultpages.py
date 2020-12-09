#!/usr/bin/python
# coding=utf-8
import ftplib


def returnDefault(ftp):
    try:
        # nlst()方法获取目录下的文件
        dirList = ftp.nlst()
    except:
        dirList = []
        print('[-] Could not list directory contents.')
        print('[-] Skipping To Next Target.')
        return

    retList = []
    for filename in dirList:
        # lower()方法将文件名都转换为小写的形式
        fn = filename.lower()
        if '.php' in fn or '.asp' in fn or '.htm' in fn:
            print('[+] Found default page: ' + filename)
            retList.append(filename)
    return retList


host = '10.10.10.130'
username = 'ftpuser'
password = 'ftppassword'
ftp = ftplib.FTP(host)
ftp.login(username, password)
returnDefault(ftp)