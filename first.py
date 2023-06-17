#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import json
import requests
import time
import random
import yaml
from datetime import datetime
import warnings
import sys
import os
warnings.filterwarnings('ignore')

def main(points='',dofile=''):
    cookiepoint=1

    if not dofile:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{timestamp}.csv'
        with open(filename, "w",encoding='utf-8-sig') as f:
            f.write("公众号fakeid,简介digest,标题title,创建时间time,链接url\n")
    else:
        if os.path.exists(dofile):
            filename = dofile
            print(f'{filename}')
        else:
            print(f'{dofile}' + ',文件不存在')
            return
    with open("cookies.yaml", "r") as file:
        file_data = file.read()
    config = yaml.safe_load(file_data) 

    headers = {
        "Cookie": config['cookie'],
        "User-Agent": config['user-agent'] 
    }

    daysbetween=config['daysbetween']

    with open("fakeids.yaml", "r") as file:
        fakeitems = yaml.load(file, Loader=yaml.FullLoader)
    count = len(fakeitems)
    if points:
        #print(int(points))
        try:
            points = int(points)
        except ValueError:
            print(f'{points} 不是有效的参数，参数需要整数')
            return
        if points > count:
            print('参数大于有效值')
            return
        else:
            count=count-points
        fakeitems=fakeitems[int(points):]
    i=1
    for fakeitem in fakeitems:
        with open(filename,'r') as f:
            for line in f:
                last_line=line
        if last_line and last_line.strip(): #判断excel最后一行是否为空，如果不为空add一条空行
            with open(filename, "a",encoding='utf-8-sig') as f:
                f.write('\n')
        
        print(f'\rProgress:{str(i)}/{str(count)}',end='')
        url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
        begin="0"
        params = {
            "action": "list_ex",
            "begin": begin,
            "count": "5",
            "fakeid": fakeitem,
            "type": "9",
            "token": config['token'],
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1"
        }
        app_msg_list = []
        time.sleep(random.randint(10,15))
        resp = requests.get(url, headers=headers, params = params, verify=False).json()
        #print(resp)
        if(resp['base_resp']['ret'] == 200013):
            print("----------被限流啦,一个小时以后重试-------------")
            print("-----------下次执行参数 "+ f'python3 first.py {str(i-1)} {filename}' + "----------")
            break
        if(resp['base_resp']['ret'] == 200003):
            print("----------session 过期啦-，请检查token或者cookie-----------")
            break
        #with open("aaaa.txt", "w",encoding='utf-8-sig') as ff:
                   #     ff.write(json.dumps(resp,ensure_ascii=False))
        if "app_msg_list" in resp:
                for item in resp["app_msg_list"]:
                    #create_time=time.localtime(item['create_time'])
                    createtime=item['create_time']
                    create_time=datetime.fromtimestamp(createtime)
                    create_time_date=create_time.date()
                    today=datetime.now().date()
                    #print(item)
                    if (today-create_time_date).days <= daysbetween:
                    #print(f'{createtime}' + "," +create_time)
                        info = '"{}","{}","{}","{}",{}'.format(fakeitem, item['digest'],item['title'], create_time, item['link'])
                        with open(filename, "a",encoding='utf-8-sig') as f:
                         f.write(info+'\n')
        i+=1                 
    print("\n"+"执行完毕！")

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)
