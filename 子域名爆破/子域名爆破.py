# -*- coding:UTF-8 -*-

import gevent.monkey
gevent.monkey.patch_all()
import warnings
warnings.simplefilter("ignore", category=UserWarning)

import optparse
import dns.resolver
import xlwt
import xlrd
import time
import requests
import queue
import re
from Tools import ProgressBar


class Excel(object):

    def __init__(self, domain):
        self.excel_file_name = domain + '-' + time.strftime("%Y%m%d%H%M", time.localtime()) + '的信息收集' + '.xlsx'
        self.xls = xlwt.Workbook()
        self.sheet1 = self.xls.add_sheet(domain, cell_overwrite_ok=True)
        self.xls.save(self.excel_file_name)

    # 设置表格样式
    def setStyle(self, name, size, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = size
        style.font = font
        return style

    def getMaxRows(self):
        rb = xlrd.open_workbook(self.excel_file_name, formatting_info=True)
        sheet = rb.sheet_by_index(0)
        nrows = sheet.nrows
        return nrows

class SubDomain(object):

    def __init__(self):
        self.rsv = dns.resolver.Resolver()
        # self.rsv.timeout = 10
        # self.rsv.lifetime = 10

    def run(self):
        while not task_queue.empty():
            domain = task_queue.get()
            for _ in range(3):
                try:
                    answers = self.rsv.query(domain)
                    if answers:
                        http = False
                        now_row = excel.getMaxRows()
                        excel.sheet1.write(now_row, 0, domain)
                        excel.xls.save(excel.excel_file_name)

                        # region HTTP
                        try:
                            request_domain = 'http://' + domain
                            response = requests.get(request_domain, allow_redirects=True, timeout=30, stream=True)
                            response.encoding = 'utf-8'
                            ip = response.raw._connection.sock.getpeername()[0]
                            title = re.search("(?<=<title>).+?(?=</title>)", response.text, re.DOTALL | re.I).group().strip()
                            excel.sheet1.write(now_row, 0, request_domain)
                            excel.sheet1.write(now_row, 1, ip)
                            excel.sheet1.write(now_row, 2, response.status_code)
                            excel.sheet1.write(now_row, 3, title)
                            excel.xls.save(excel.excel_file_name)
                            print(request_domain, response.status_code, ip, title)
                            http = True
                        except requests.ConnectionError as e:
                            pass
                        except Exception as e:
                            print(e)
                        # endregion

                        # region HTTPS
                        if http == False:
                            try:
                                request_domain = 'https://' + domain
                                response = requests.get(request_domain, allow_redirects=True, timeout=30, stream=True)
                                response.encoding = 'utf-8'
                                ip = response.raw._connection.sock.getpeername()[0]
                                title = re.search("(?<=<title>).+?(?=</title>)", response.text, re.DOTALL | re.I).group().strip()
                                excel.sheet1.write(now_row, 0, request_domain)
                                excel.sheet1.write(now_row, 1, ip)
                                excel.sheet1.write(now_row, 2, response.status_code)
                                excel.sheet1.write(now_row, 3, title)
                                excel.xls.save(excel.excel_file_name)
                                print(request_domain, response.status_code, ip, title)
                            except requests.ConnectionError as e:
                                pass
                            except Exception as e:
                                print(e)
                        # endregion
                        break
                except dns.resolver.NoNameservers as e:
                    break
                except Exception as e:
                    if re.search('The DNS response does not contain an answer to the question', str(e), re.I):
                        pass
                    elif re.search('The DNS operation timed out after', str(e), re.I):
                        pass
                    else:
                        print(domain, e)
            progress_bar.show(task_queue.qsize())

if __name__ == "__main__":

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

    options.domain = "vulbox.com"
    options.gnum = 30

    # region 初始化excel
    excel = Excel(options.domain)
    title = ['URL', 'IP地址', '状态', '标题']
    for i in range(0, len(title)):
        excel.sheet1.write(excel.getMaxRows(), i, title[i], excel.setStyle('Microsoft YaHei', 200, True))
    excel.xls.save(excel.excel_file_name)
    # endregion

    # region 载入数据到队列
    task_queue = queue.Queue()
    with open('subdomain-list.txt', 'r') as f:
        line = f.readline()
        while line:
            task_queue.put(line.strip() + '.' + options.domain)
            line = f.readline()
    progress_bar = ProgressBar.Bar(task_queue.qsize())
    # endregion

    # gevent
    start = time.time()
    jobs = []
    for i in range(options.gnum ):
        jobs.append(gevent.spawn(SubDomain().run))
    gevent.joinall(jobs)
    print(time.time() - start)
    # endregion