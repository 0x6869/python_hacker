'''
通过访问注册表，获取用户连接过的wifi热点和其MAC地址
'''
# coding=utf-8
from winreg import *


# 将REG_BINARY值转换成一个实际的Mac地址
def val2addr(val):
    addr = ""
    for ch in val:
        addr += ("%02x " % ch)
    addr = addr.strip(" ").replace(" ", ":")[0:17]
    return addr


# 打印网络相关信息
def printNets():
    net = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    print("\n[*]Networks You have Joined.")
    for i in range(100):
        try:
            guid = EnumKey(key, i)
            netKey = OpenKey(key, str(guid))
            (n, addr, t) = EnumValue(netKey, 5)
            (n, name, t) = EnumValue(netKey, 4)
            macAddr = val2addr(addr)
            netName = name
            print('[+] ' + netName + '  ' + macAddr)
            CloseKey(netKey)
        except:
            continue


def main():
    printNets()


if __name__ == '__main__':
    main()