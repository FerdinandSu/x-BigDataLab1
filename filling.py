 #from imdb import Cinemagoer
import pandas as pd
import numpy as np
import os
import math
import logging
import time
from imdb_utils import get_movie_info_by_title
import json

if os.path.exists('fill_black_list.json'):
    with open('fill_black_list.json','r',encoding='utf8') as f:
        blacklist=json.load(f)
else: blacklist=[]
blacklist=set(blacklist)

def save_blacklist():
    with open('fill_black_list.json','w',encoding='utf8') as f:
        json.dump([s for s in blacklist],f)    

logging.basicConfig(level=logging.INFO)

data = pd.read_csv('movies2.csv')

total_fill=0

for index, row in data.iterrows():
    if row is None: continue
# 遍历每一行的每一个字段
    for column, value in row.iteritems():
        if value == 0 or value == None or value == '0' :
            print(f"({row['movie_id']},{column}) shoule be replaced")
            total_fill += 1

processed_fill=0
success_fill=0
start=time.time()

def get_eta():
    elapsed = time.time() - start
    remaining = (total_fill - processed_fill) * elapsed / processed_fill
    eta = math.ceil(remaining)
    return str(eta) +'s'

# Count all
for index, row in data.iterrows():
    try :
        if row is None: continue
        info=None
        skip_flag=False
    # 遍历每一行的每一个字段
        for column, value in row.iteritems():
            blk_str=f'{index}-{column}'
            if blk_str in blacklist or skip_flag: 
                processed_fill += 1
                continue
            if value == 0 or value == None or value == '0' :
                print(f"({row['movie_id']},{column}) shoule be replaced")
                if info is None: 
                    info = get_movie_info_by_title(row['title'])
                if info is None: 
                    logging.warning(f"Movie :({row['title']},{column}) patch failed Added to Blacklist.")
                    blacklist.add(blk_str)
                    save_blacklist()
                    skip_flag=True
                    processed_fill+=1
                    continue # whole line failed
                value=info[column]
                data.loc[index,column] = value
                processed_fill+=1
                success_fill+=1
                eta=get_eta()
                logging.info(f"PATCH: ({row['title']},{column}) <- {value}  ({processed_fill}/{total_fill}), {success_fill} successed, {eta} remaining")
                data.to_csv('movies2.csv')
    except Exception as e:
        print("An error occurred:", e)


            



