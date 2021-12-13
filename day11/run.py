import pandas as pd
import numpy as np
from pathlib import Path
import itertools
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
from operator import is_not
from functools import partial
import logging

# create file handler which logs even debug messages
logging.basicConfig(filename=Path(__file__).parent / 'output.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
day = 'Day 11'
logging.info(f"{day} - Dumbo Octopuses")
logger = logging.getLogger(day)

# inputfile = Path(__file__).parent / 'input_sample.csv'
inputfile = Path(__file__).parent / 'input.csv'

data = []
data = pd.read_csv(inputfile, header=None, dtype=str)
data = data[0].apply(lambda x: pd.Series(list(x)))
data = data.astype(int)

def find_adjancent(data, x, y): 
    adj_lookup = [[col + y, row + x] for row in (-1,0,1) for col in (-1,0,1) if [row + x, col + y] != [x,y]] 
    # the order comes out as NW, W, SW, N, S, NE, E, SE

    # TODO: map to a better order of N, NE, E, SE, S, SW, W, NW
    adj_values = []
    for index, adj in enumerate(adj_lookup):
        if adj[0] < 0 or adj[1] < 0 or adj[0] > data.shape[1] - 1 or adj[1] > data.shape[0] - 1:
            adj_values.append(None)
        else:
            adj_values.append(data.at[adj[0], adj[1]])

    return data.at[y,x], adj_values
     
def inc_neighbors(data, x, y):
    adj_lookup = [[col + y, row + x] for row in (-1,0,1) for col in (-1,0,1) if [row + x, col + y] != [x,y]] 
    # the order comes out as NW, W, SW, N, S, NE, E, SE

    inc_array = []
    for index, adj in enumerate(adj_lookup):
        if adj[0] < 0 or adj[1] < 0 or adj[0] > data.shape[1] - 1 or adj[1] > data.shape[0] - 1:
            pass
        else:
            data.at[adj[0], adj[1]] += 1
            # Check if this is a new flash, or just incrementing past 10
            new = False
            if data.at[adj[0], adj[1]] == 10:
                new = True
            else:
                new = False
            inc_array.append([new, adj[1], adj[0], data.at[adj[0], adj[1]]])

    return inc_array


def resolve_flashes(data):
    result = {
        "new_flash_count": 0,
    }

    processed_flash = ~(data >= 10)
    while processed_flash.all(axis=None) == False:
        # print("iterating")
        for y in range(0, data.shape[0]):
            for x in range(0, data.shape[1]):
                if not processed_flash.at[y, x]:
                    for new_flash in inc_neighbors(data, x, y):
                        if new_flash[0]:
                            processed_flash.at[new_flash[2], new_flash[1]] = False
                            
                        # else:
                            # processed_flash.at[new_flash[2], new_flash[1]] = True

                    processed_flash.at[y, x] = True  
    
    # now reset the frame back to 0's for the flashed elements!
    result['new_flash_count'] += data[data >= 10].count().sum()
    data[data >= 10] = 0
    return result 
    
totals = 0
sync_iter = None
for step in range(0, 1000):
    print(f"iterating on step {step}")
    data += 1
    print(data)
    r = resolve_flashes(data)
    print(data)
    if step < 100:
        totals += r['new_flash_count']

    # check if synchronous
    sync_count = 0
    sync_count = data[data == 0].count().sum()
    print(sync_count)
    
        
    if sync_count == 100:
        sync_iter = step+1
        break 

print(f'Part 1 has {totals} flashes')
print(f'Part 2 synchronized at iter {sync_iter}')
