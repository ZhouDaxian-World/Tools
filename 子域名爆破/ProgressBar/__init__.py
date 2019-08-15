# coding:utf-8

import sys,time
from colorama import Fore

class Bar:

    buff = ''

    def __init__(self, total, width=160):
        self.start_time = time.time()
        self.total = total
        self.width = width

    def show(self, count):
        bar_width = int(self.width * (self.total - count) / self.total)
        bar_1_len, bar_2_len = divmod(bar_width, 8)
        l_bar = '{0:3.0f}%|'.format(((self.total - count) / self.total) * 100)
        speed_bar = str(int(time.time() - self.start_time)) + 's | '
        speed_bar += '{0:5.2f}'.format((self.total - count) / (time.time() - self.start_time)) if time.time() - self.start_time else '?'
        speed_bar += 'it/s'
        r_bar = '| {0}/{1} | '.format((self.total - count), self.total) + speed_bar

        bar = ''
        if bar_1_len:
            bar += (chr(0x2588) * bar_1_len)
        if bar_2_len:
            bar += (chr(0x2590 - bar_2_len))
        bar += ' ' * (int(self.width / 8) - bar_1_len)

        sys.stdout.write("\r")
        bar = Fore.RED + l_bar + bar + r_bar + Fore.BLACK
        sys.stdout.write(bar)
        sys.stdout.flush()