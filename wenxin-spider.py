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
    if not dofile:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{timestamp}.csv'
        with open(filename, "w",encoding='utf-8-sig') as f:
            f.write("公众号fakeid,简介digest,标题title,创建时间time,链接url\n")
    else:
        if os.path.exists(dofile):
            filename = dofile
            print(f'将使用 {filename}')
        else:
            print(f'{dofile}' + ',文件不存在')
            return
    with open("cookies.yaml", "r") as file:
        file_data = file.read()
    config = yaml.safe_load(file_data) 

    

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
   # k=0
    cookiepointstart=0
    cookiepoint=0
    cookiecount=0
    today=datetime.now().date()
    for fakeitem in fakeitems:
        with open(filename,'r') as f:
            for line in f:
                last_line=line
        if last_line and last_line.strip(): #判断excel最后一行是否为空，如果不为空add一条空行
            with open(filename, "a",encoding='utf-8-sig') as f:
                f.write('\n')


        if isinstance(config['token'],list):
            tokens_legth=len(config['token'])
        else:
            print("Cookie 读取错误，请检查")
            break
        validcookie=[False]*tokens_legth
        checkcookieOK=False
        donextpoint=False        
        while checkcookieOK == False:
            print(f"检查账号是否被封禁")
            #time.sleep(3)
            if cookiepointstart % config['accountmaxdo'] == 0 or donextpoint == True:
                cookiepoint= cookiecount % tokens_legth
                cookiecount+=1
                donextpoint=False

            url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
            begin="0"
            params = {
                "action": "list_ex",
                "begin": begin,
                "count": "5",
                "fakeid": fakeitem,
                "type": "9",
                "token": config['token'][cookiepoint],
                "lang": "zh_CN",
                "f": "json",
                "ajax": "1"
            }
            #print(f"现在正在用的fakeitem={fakeitem}")
            headers = {
            "Cookie": config['cookie'][cookiepoint],
            "User-Agent": config['user-agent'] 
            }


            app_msg_list = []

            resp = requests.get(url, headers=headers, params = params, verify=False).json()
            time.sleep(random.randint(3,5))
            #print('爬取远程数据')
            #resp = {'base_resp': {}}
            '''
            if k == 0:
                resp['base_resp']['ret'] = 200013
            else:
                resp['base_resp']['ret'] = 200000
            '''
            if(resp['base_resp']['ret'] == 200013):
                print(f"----------第{str(cookiepoint)}个账号被限流啦,正在尝试下一个账号-------------")
                print("-----------手工执行参数 "+ f'python3 wenxin-spider.py {str(i-1)} {filename}' + "----------")
                validcookie[cookiepoint]=True
                checkcookieOK=False
                donextpoint=True
               # print(f"fdsafasfsa={str(all(validcookie))}")
            elif(resp['base_resp']['ret'] == 200003):
                print(f"----------第{str(cookiepoint)}个账号session 过期啦，请检查token或者cookie-----------")
                print("-----------手工执行参数 "+ f'python3 wenxin-spider.py {str(i-1)} {filename}' + "----------")
                break
            else:
                checkcookieOK = True
                print(f"第{str(cookiepoint)}个账号状态正常！可以继续！")
                time.sleep(1)

            if  all(validcookie):
                print(f"--------所有{str(tokens_legth)}个账号都被限流啦,正在等待15分钟再试，现在时间{str(datetime.now())}------------")
                time.sleep(900)
                #k=1
                validcookie=[False]*tokens_legth
                checkcookieOK == False
                donextpoint=False

        print(f'\rProgress:{str(i)}/{str(count)}',end='')
        
        if "app_msg_list" in resp:
            for item in resp["app_msg_list"]:
                #create_time=time.localtime(item['create_time'])
                createtime=item['create_time']
                create_time=datetime.fromtimestamp(createtime)
                create_time_date=create_time.date()
                #print(item)
                if (today-create_time_date).days <= daysbetween:
                #print(f'{createtime}' + "," +create_time)
                    info = '"{}","{}","{}","{}",{}'.format(fakeitem, item['digest'],item['title'], create_time, item['link'])
                    with open(filename, "a",encoding='utf-8-sig') as f:
                     f.write(info+'\n')
        i+=1
        cookiepointstart +=1
        #print(f"{str(fakeitem)}执行完毕，等待下一个执行")         
        time.sleep(random.randint(15,30))
    print("\n"+"执行完毕！")

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)
