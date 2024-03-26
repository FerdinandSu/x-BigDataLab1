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

def save_data():
    data.to_csv('movies2.csv')

class Counter(object):
    def __init__(self,total_fill):
        self.processed_fill=0
        self.success_fill=0
        self.start=time.time()
        self.total_fill=total_fill

    def get_eta(self):
        elapsed = time.time() - self.start
        remaining = (self.total_fill - self.processed_fill) * elapsed / self.processed_fill
        eta = math.ceil(remaining)
        return str(eta) +'s'

    def step_failed(self):
        self.processed_fill += 1
    def step_success(self):
        self.processed_fill += 1
        self.success_fill += 1

# Count all
import concurrent.futures

def process_row(row, counter: Counter):
    try:
        if row is None:
            return
        info = None
        skip_flag = False
        for column, value in row.iteritems():
            blk_str = f'{index}-{column}'
            if blk_str in blacklist or skip_flag:
                counter.step_failed()
                continue
            if value == 0 or value == None or value == '0':
                print(f"({row['movie_id']},{column}) should be replaced")
                if info is None:
                    info = get_movie_info_by_title(row['title'])
                if info is None:
                    logging.warning(f"Movie: ({row['title']},{column}) patch failed. Added to Blacklist.")
                    blacklist.add(blk_str)
                    save_blacklist()
                    skip_flag = True
                    counter.step_failed()
                    continue  # whole line failed
                value = info[column]
                data.loc[index, column] = value
                counter.step_success()
                eta = counter.get_eta()
                logging.info(f"PATCH: ({row['title']},{column}) <- {value}  ({counter.processed_fill}/{counter.total_fill}), {counter.success_fill} succeeded, {eta} remaining")
                save_data()
    except Exception as e:
        print("An error occurred:", e)

def process_rows():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        counter=Counter(total_fill)
        futures = []
        for index, row in data.iterrows():
            futures.append(executor.submit(process_row, row, counter))
        for future in concurrent.futures.as_completed(futures):
            future.result()

process_rows()


            



