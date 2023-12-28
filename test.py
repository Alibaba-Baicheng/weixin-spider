#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import json
import requests
import time
import random
import yaml
from datetime import datetime
from time import sleep

#timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#filename = f'{timestamp}.txt'
with open("cookies.yaml", "r") as file:
    file_data = file.read()

config = yaml.safe_load(file_data) 
daysbetween=config['daysbetween']

a=1686727270
#create_time=time.localtime(a)
#print(create_time)
#create_time=time.strftime("%Y-%m-%d",create_time)
create_time=datetime.fromtimestamp(a)
create_time_date=create_time.date()
today=datetime.now().date()
print((today-create_time_date).days)
if (today-create_time_date).days <= daysbetween:
	print(create_time.date())
else:
	print('OK')
#json_name = "mp_data.jso<"
#print(filename)

with open("fakeids.yaml", "r") as file:
    file_data = yaml.load(file, Loader=yaml.FullLoader)
    count = len(file_data)
i=1
for item in file_data:
	#if isinstance(item,list):
	#	for subitem in item:
	#		print(subitem)
	#else:
		#print(item)
		#print(str(i)+"/"+str(count))
		#print(f'\rProgress:{i/count*100:.0f}%',end='')
		#print(f'\rProgress:{str(i)}/{str(count)}',end='')
		i+=1
		#sleep(0.1)
#for i in range(10):
 #   print(f'\rProgress: {i+1}/10', end=' ')
  #  sleep(0.5)

with open("cookies-2.yaml", "r") as file:
   file_data = file.read()
config = yaml.safe_load(file_data)
if isinstance(config['token'],list):
	tokens_legth=len(config['token'])
for tokenpoint in range(tokens_legth):
	print(config["token"][tokenpoint])
	#print(f'{tokens_legth}')
print(config['token'])

with open("cookies.yaml", "r") as file:
   file_data = file.read()
config = yaml.safe_load(file_data)
print(config['token'])
#for cookie in config['cookie']:
#	print(cookie['expires'])
