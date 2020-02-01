#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author : Lakr Aream, AloneMonkey(frida-iOS-dump)
# me 233:       https://www.qaq.wiki, Twitter: @Lak233
# big uncle:    http://www.alonemonkey.com

# 非常感谢庆总让iOS逆向的门槛降低到无脑级别

import sys
import codecs
import frida
import threading
import os
import shutil
import time
import argparse
import tempfile
import subprocess
import re

import paramiko
from paramiko import SSHClient
from scp import SCPClient
from tqdm import tqdm
import traceback

if (len(sys.argv) < 2):
    print("-> ./lsapps.py [iDevices UDID]")
    exit(-1)

if (len(sys.argv) > 2):
    print("-> ./lsapps.py [iDevices UDID]x1")
    exit(-1)

def get_usb_iphone():
    Type = 'usb'
    if int(frida.__version__.split('.')[0]) < 12:
        Type = 'tether'
    device_manager = frida.get_device_manager()
    changed = threading.Event()

    def on_changed():
        changed.set()

    device_manager.on('changed', on_changed)

    device = None
    while device is None:
        devices = [dev for dev in device_manager.enumerate_devices() if dev.type == Type]
        if len(devices) == 0:
            print('Waiting for USB device...')
            changed.wait()
        else:
            device = devices[0]

    device_manager.off('changed', on_changed)

    return device
