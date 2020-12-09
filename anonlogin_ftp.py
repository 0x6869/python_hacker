#!/usr/bin/python
# coding=utf-8
import ftplib


def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', '123@123.com')
        print('\n[*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    except Exception as e:
        print('\n[-] ' + str(hostname) + ' FTP Anonymous Logon Failed.')
        return False


hostname = '127.0.0.1'
anonLogin(hostname)