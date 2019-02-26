#!/usr/bin/python
# -*- coding: UTF-8 -*-

# str = r'v_sh600677="1~航天通信~600677~15.93~16.84~16.83~449291~217579~231655~15.93~16~15.92~16~15.91~5~15.90~87~15.89~46~16.00~738~16.01~89~16.02~77~16.03~33~16.04~69~10:53:30/15.93/589/S/941554/19441|10:53:26/15.97/121/B/193237/19430|10:53:24/15.93/6/S/9562/19423|10:53:22/15.93/2/S/3186/19413|10:53:19/15.97/50/B/79736/19401|10:53:16/15.90/563/S/895589/19392~20190226105333~-0.91~-5.40~16.83~15.50~15.90/447457/720747129~449291~72367~10.79~29.62~~16.83~15.50~7.90~66.34~83.12~2.48~18.52~15.16~1.71~-836~16.11~50.28~82.90";'
import re
import time
import threading

import requests
from multiprocessing import Process, Queue
import os

stoke_code = 'sh600677'


class StokeInfo:
    market = ''
    information = ''
    position = ''
    money = ''
    q = None

    def __init__(self):
        self.threadLock = threading.Lock()

    def set_market(self, market):
        self.threadLock.acquire()
        if self.market != market:
            self.market = market
            self.notify()
        self.threadLock.release()

    def set_information(self, information):
        self.threadLock.acquire()
        if self.information != information:
            self.information = information
            self.notify()
        self.threadLock.release()

    def set_position(self, position):
        self.threadLock.acquire()
        if self.position != position:
            self.position = position
            self.notify()
        self.threadLock.release()

    def set_money(self, money):
        self.threadLock.acquire()
        if self.money != money:
            self.money = money
            self.notify()
        self.threadLock.release()

    def notify(self):
        q.put(self.market)
        # if self.market != '' and self.information != '' and self.position != '' and self.money != '':
        #     print(self.market)
        #     print(self.information)
        #     print(self.position)
        #     print(self.money)


stokeInfo = StokeInfo()


class StokeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.get_stoke()

    def get_stoke(self):
        pass


class myThread1(StokeThread):
    # 要获取最新行情
    def get_stoke(self):
        resu = requests.get('http://qt.gtimg.cn/q=' + stoke_code)
        result = re.split(r'[=]', resu.text)
        info = re.sub(r'[";]', "", result[1])
        infos = re.split(r'[~]', info.strip())
        stokeInfo.set_market(str(infos))


class myThread2(StokeThread):
    # 获取实时资金流向：
    def get_stoke(self):
        resu = requests.get('http://qt.gtimg.cn/q=ff_' + stoke_code)
        result = re.split(r'[=]', resu.text)
        info = re.sub(r'[";]', "", result[1])
        infos = re.split(r'[~]', info.strip())
        stokeInfo.set_money(str(infos))


class myThread3(StokeThread):
    #  获取盘口分析：
    def get_stoke(self):
        resu = requests.get('http://qt.gtimg.cn/q=s_pk' + stoke_code)
        result = re.split(r'[=]', resu.text)
        info = re.sub(r'[";]', "", result[1])
        infos = re.split(r'[~]', info.strip())
        stokeInfo.set_position(str(infos))


class myThread4(StokeThread):
    #  获取简要信息：
    def get_stoke(self):
        resu = requests.get('http://qt.gtimg.cn/q=s_' + stoke_code)
        result = re.split(r'[=]', resu.text)
        info = re.sub(r'[";]', "", result[1])
        infos = re.split(r'[~]', info.strip())
        stokeInfo.set_information(str(infos))


def stoke(q):
    print(os.getpid())
    stokeInfo.q = q
    threads = [myThread1(), myThread2(), myThread3(), myThread4()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


q = Queue()
p_stoke = Process(target=stoke, args=(q,))
p_stoke.start()

print(os.getpid())
while True:
    value = q.get(True)
    print('Get %s from queue.' % value)
