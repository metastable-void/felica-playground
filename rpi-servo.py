# coding: utf-8
import nfc
import binascii
import time
from threading import Thread, Timer

import RPi.GPIO as GPIO
import time
import signal
import os

dirname = os.path.dirname(os.path.abspath(__file__))

idm_list = []
try:
    with open(dirname + '/idm-list.txt') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            if line == '':
                continue
            idm_list.append(line.lower())
except IOError:
    pass


servopin = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin,50)
p.start(0)
time.sleep(2)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servopin, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servopin, False)
    p.ChangeDutyCycle(0)

def check_idm(idm):
    if idm in idm_list:
        SetAngle(170)

# 待ち受けの1サイクル秒
TIME_cycle = 10.0
# 待ち受けの反応インターバル秒
TIME_interval = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 3

# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
target_req_felica = nfc.clf.RemoteTarget("212F")

def int_to_hex(n):
    return "0x%0.4x" % n

def check_FeliCa():
    print 'POLLING: Type-F/FeliCa'
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')
    # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
    target_res = clf.sense(target_req_felica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
    if not target_res is None:
        tag = nfc.tag.activate(clf, target_res)

        #IDmを取り出す
        idm = binascii.hexlify(tag.idm)
        sys = tag.sys
        print 'RESPONSE: sys=' + int_to_hex(sys) + ' idm=' + idm
        check_idm(idm)
        
        try:
            idm, pmm = tag.polling(system_code=0x0003)
            idm = binascii.hexlify(idm)
            print 'DISCOVERED: sys=0x0003/suica_compat idm=' + idm
            check_idm(idm)
        except nfc.tag.tt3.Type3TagCommandError:
            pass

        try:
            idm, pmm = tag.polling(system_code=0x832c)
            idm = binascii.hexlify(idm)
            print 'DISCOVERED: sys=0x832c/ecomyca idm=' + idm
            check_idm(idm)
        except nfc.tag.tt3.Type3TagCommandError:
            pass

        try:
            idm, pmm = tag.polling(system_code=0x8592)
            idm = binascii.hexlify(idm)
            print 'DISCOVERED: sys=0x8592/paspy idm=' + idm
            check_idm(idm)
        except nfc.tag.tt3.Type3TagCommandError:
            pass

        try:
            idm, pmm = tag.polling(system_code=0x865e)
            idm = binascii.hexlify(idm)
            print 'DISCOVERED: sys=0x865e/sapica idm=' + idm
            check_idm(idm)
        except nfc.tag.tt3.Type3TagCommandError:
            pass

        try:
            idm, pmm = tag.polling(system_code=0x12fc)
            idm = binascii.hexlify(idm)
            print 'DISCOVERED: sys=0x12fc/ndef idm=' + idm
            check_idm(idm)
        except nfc.tag.tt3.Type3TagCommandError:
            pass

        try:
            idm, pmm = tag.polling(system_code=0xfe00)
            idm = binascii.hexlify(idm)
            print 'DISCOVERED: sys=0xfe00/common idm=' + idm
            check_idm(idm)
        except nfc.tag.tt3.Type3TagCommandError:
            pass

        try:
            idm, pmm = tag.polling(system_code=0x88b4)
            idm = binascii.hexlify(idm)
            print 'DISCOVERED: sys=0x88b4/lite_s idm=' + idm
            check_idm(idm)
        except nfc.tag.tt3.Type3TagCommandError:
            pass

        try:
            idm, pmm = tag.polling(system_code=0x957a)
            idm = binascii.hexlify(idm)
            print 'DISCOVERED: sys=0x957a/secure_id idm=' + idm
            check_idm(idm)
        except nfc.tag.tt3.Type3TagCommandError:
            pass

        #sleepなしでは次の読み込みが始まって終了する
        print 'QUIT'
        time.sleep(TIME_wait)

    clf.close()

try:
    while True:
        SetAngle(80)
        check_FeliCa()
except KeyboardInterrupt:
    pass

GPIO.cleanup()

