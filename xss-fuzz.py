# -*- coding:UTF-8 -*-

import gevent.monkey
gevent.monkey.patch_all()
import warnings
warnings.simplefilter("ignore", category=UserWarning)

import optparse
xssFuzzList = [
    ]

class Scan(object):

    def run(self):
        pass

def main():
    # region 解释命令行
    parse = optparse.OptionParser(usage='usage:%prog [options] --domain 域名 --gevent 协程数', version='%prog 1.0')
    parse.prog = '子域名收集'
    parse.add_option('--url', dest='url', action='url', type=str, metavar='domain', help='域名')
    parse.add_option('--gevent', dest='gevent', action='store', type=int, metavar='gnum', help='域名')
    options, args = parse.parse_args()
    # endregion

    options.url = "http://xxx.com"
    options.method = "GET"
    options.data = "xxx=?&xxx=?&xxx=?"




if __name__ == "__main__":
    @TODO 寻找xss过滤的方法，反推得到xss字符
    main()
