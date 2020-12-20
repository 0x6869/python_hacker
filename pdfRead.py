# coding=utf-8
'''
提取pdf文件元数据
'''

import optparse
from PyPDF2 import PdfFileReader


# 使用getDocumentInfo()函数提取PDF文档所有的元数据
def printMeta(fileName):
    pdfFile = PdfFileReader(open(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    print("[*] PDF MeataData For: " + str(fileName))
    for meraItem in docInfo:
        print("[+] " + meraItem + ": " + docInfo[meraItem])


def main():
    parser = optparse.OptionParser("[*]Usage: python pdfread.py -F <PDF file name>")
    parser.add_option('-F', dest='fileName', type='string', help='specify PDF file name')
    (options, args) = parser.parse_args()
    fileName = options.fileName
    if fileName == None:
        print(parser.usage)
        exit(0)
    else:
        printMeta(fileName)


if __name__ == '__main__':
    main()
