# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/11/27 12:36
# 自动抢车位
'''
new Env('自动抢车位');
cron=0 1 21 ? * sat  python3 Grab_parking_space.py
'''

import os, re, time
try:
    from telethon import TelegramClient
except Exception as e:
    print(e, "\n缺少telethon模块")
    exit(3)
########################修改这一段############################
phone_number = '' # telegram手机号
api_id = '' # 用户api_id
api_hash = '' # 用户 api_hash
bot_name = '' # 助力池机器人名称，例如：@jdsharebot
# 根据自己的需求在code.sh中获取相应的名称,格式为 name_config:提交代码
fileNames = {'Bean':'/bean',        # 种豆得豆
             'JdFactory':'/ddfactory',       # 东东工厂
             'Fruit': '/farm',      # 京东农场
             'Health': '/health',      # 京东健康
             'DreamFactory': '/jxfactory',        # 京喜工厂
             'Pet': '/pet',     # 京东萌宠
             'Sgmh': '/sgmh'     # 闪购盲盒
             }
##############################################################
# 这下面不用管
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def findCode():
    allcode = {}
    reRule = re.compile(r"(?<=').+(?=')")
    for fileName in fileNames:
        try:
            with open('/ql/log/.ShareCode/' + fileName + '.log', 'r', encoding='utf-8') as f:
                context = f.read()
        except Exception as e:
            print(e, '未找到%s日志文件，请确认运行过code.sh。' % fileName)
            continue
        allcode[fileName] = '&'.join(reRule.findall(context))
    return allcode

class Telegram:
    def __init__(self,api_id,api_hash,phoneNumber):
        session_name = "id_" +api_id
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.client.start(phoneNumber)
    def sendms(self,bot_name,ms):
        self.client.loop.run_until_complete(self.client.send_message(bot_name, ms))
        time.sleep(1)
        self.client.loop.run_until_complete(self.client.send_read_acknowledge(bot_name))
        print("提交成功")

if __name__ == '__main__':
    allcode = findCode()
    tele = Telegram(api_id,api_hash,phone_number)
    for each_code in allcode:
        massage = fileNames[each_code]+' '+allcode[each_code]
        tele.sendms(bot_name,massage)
        print('%s已发送'%each_code)
    print('运行完成')
    exit(0)
