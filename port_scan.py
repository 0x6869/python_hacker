#!/usr/bin/env

'''
利用nmap模块进行端口扫描
'''

import  nmap
import optparse

def nmapScan(tgtHost,tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost,tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print("[*] " + tgtHost + " tcp/" + tgtPort + " " + state)

def main():
    parser = optparse.OptionParser('%prog -H <target host> -p <target port>')
    parser.add_option('-H','--host',dest='tgtHost',type='string',help='specify target host')
    parser.add_option('-p','--port',dest = 'tgtPorts',type='string',\
                      help='specify target port[s] separated by comma')
    (options,args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPorts).split(', ')
    if tgtHost == None or tgtPorts[0] == 'None':
        print(parser.usage)
        exit(0)
        print(args)
    for port in tgtPorts:
        nmapScan(tgtHost,port)

if __name__ == '__main__':
    main()
