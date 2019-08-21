# -*- coding:UTF-8 -*-

import gevent.monkey
gevent.monkey.patch_all()
import warnings
warnings.simplefilter("ignore", category=UserWarning)

import optparse
import xlrd
import requests
import queue
import time


url = ["/.git/config", "/.svn/entries"]


class Scan(object):

    def run(self, values):
        gitUrl = "http://" + values + "/.git/config"
        try:
            response = requests.get(gitUrl, timeout=5)
            if response.status_code == 200:
                pass
        except Exception as e:
            pass

        svnUrl = "http://" + values + "/.svn/entries"
        try:
            response = requests.get(gitUrl, timeout=5)
            if response.status_code == 200:
                pass
        except Exception as e:
            pass



def main():
    # region 解释命令行
    parse = optparse.OptionParser(usage='usage:%prog [options] --domain 域名 --gevent 协程数', version='%prog 1.0')
    parse.prog = '子域名收集'
    parse.add_option('--domain', dest='domain', action='store', type=str, metavar='domain', help='域名')
    parse.add_option('--gevent', dest='gevent', action='store', type=int, metavar='gnum', help='域名')
    options, args = parse.parse_args()
    # endregion

    # if not options.domain:
    #     parse.error('必须输入要收集的域名')
    # if not options.thread:
    #     options.thread = 1

    # options.domain = "vulbox.com"
    # options.gnum = 30



    # gevent
    start = time.time()
    jobs = []
    for i in range(options.gnum):
        jobs.append(gevent.spawn(Scan().run))
    gevent.joinall(jobs)
    print(time.time() - start)
    # endregion



if __name__ == "__main__":
    main()

