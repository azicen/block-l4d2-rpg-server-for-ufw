#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import shutil
import json
import requests
from typing import List

RPGLIST_URL = 'https://yxnan.cn/misc/rpglist.json'
TMP = '/tmp/block-l4d2-rpg-server-for-ufw'
RPGLIST_SAVE_PATH = os.path.join(TMP, 'rpglist.json')

class RPGItem:
    ip: str
    note: str

    def __init__(self, ip: str, note: str) -> None:
        self.ip = ip
        self.note = note
        pass

    pass


# 下载文件
def download(url: str, file_path: str):
    with open(file_path, 'w') as file:
        req = requests.get(url)
        file.write(str(req.content, encoding='utf8'))
        file.close()
    pass

# 读取rpg服务器列表
def read_rpg_list(rpg_list_json_path: str) -> List[RPGItem]:
    file = open(rpg_list_json_path, 'r')
    content_json = file.read()
    content = json.loads(content_json)
    list = []
    for data in content['data']:
        list.append(RPGItem(data['raddr'], data['memo']))
    return list

# 生成ufw命令start_sh文件
def generate_start_sh(rpg_list: List[RPGItem], start_sh_path: str):
    file = open(start_sh_path, 'w')
    file.write('#!/bin/sh\n\n')

    for item in rpg_list:
        file.write(f'ufw reject out from any to {item.ip} comment "{item.note}"\n')

    file.close()
    pass

# 生成ufw命令stop_sh文件
def generate_stop_sh(rpg_list: List[RPGItem], stop_sh_path: str):
    file = open(stop_sh_path, 'w')
    file.write('#!/bin/sh\n\n')

    for item in rpg_list:
        file.write(f'ufw delete reject out from any to {item.ip} comment "{item.note}"\n')

    file.close()
    pass

# 生成gufw的规则导入文件
def generate_gufw_profile(rpg_list: List[RPGItem], gufw_profile_path: str):
    file = open(gufw_profile_path, 'w')
    file.write(
'''[fwBasic]
status = enabled
incoming = reject
outgoing = allow
routed = disabled

'''
    )

    i = 0
    for item in rpg_list:
        file.write(
f'''[Rule{i}]
ufw_rule = "REJECT {item.ip}"
description =
command = /usr/sbin/ufw reject out from any to {item.ip} comment "{item.note}"
policy = reject
direction = out
protocol =
from_ip =
from_port =
to_ip = {item.ip}
to_port =
iface =
routed =
logging =

'''
        )
        i+=1

    file.close()
    pass


if __name__ == '__main__':
    # 清理临时目录
    if os.path.exists(TMP):
        shutil.rmtree(TMP)
    os.mkdir(TMP)

    gen_path = os.path.join(os.getcwd(), 'gen')
    # 清理生成目录
    if os.path.exists(gen_path):
        shutil.rmtree(gen_path)
    os.mkdir(gen_path)

    # 下载rpg服务器列表
    download(RPGLIST_URL, RPGLIST_SAVE_PATH)

    list = read_rpg_list(RPGLIST_SAVE_PATH)

    start_sh_path = os.path.join(gen_path, 'start.sh')
    generate_start_sh(list, start_sh_path)

    stop_sh_path = os.path.join(gen_path, 'stop.sh')
    generate_stop_sh(list, stop_sh_path)

    gufw_profile_path = os.path.join(gen_path, 'l4d2-rpg-server.profile')
    generate_gufw_profile(list, gufw_profile_path)

    print('RPG服务器列表生成完成')

    pass
