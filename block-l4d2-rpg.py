#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import subprocess

def start():
    # 执行添加规则的脚本
    print('开始添加防火墙规则...')
    process = subprocess.Popen('sudo sh ./gen/start.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())
    process.wait()
    print('防火墙规则添加完成')
    pass

def stop():
    # 执行移除规则的脚本
    print('开始移除防火墙规则...')
    process = subprocess.Popen('sudo sh ./gen/stop.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())
    process.wait()
    print('防火墙规则移除完成')
    pass


if __name__ == '__main__':

    output = subprocess.check_output('python3 generate.py', shell=True).decode('utf-8')
    print(output)

    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "start":
                start()
            case "stop":
                stop()

    pass
