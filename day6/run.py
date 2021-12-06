import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

import logging

# create file handler which logs even debug messages
logging.basicConfig(filename=Path(__file__).parent / 'output.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Day 6 - Fishies")
logger = logging.getLogger('day6')

inputfile = Path(__file__).parent / 'input.csv'

group = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0
}
data = []
ln_count = 0
with open(inputfile) as fp:
    read_lines = fp.readlines()
    for line in read_lines:
        ln_count += 1
        if line is not None:
            line = line.strip()

        if ln_count == 1:
            # populate the object
            for fish in line.split(','):
                # print(f"Adding fish with state: {fish}")
                # group the fish
                f_int = int(fish)
                group[f_int] += 1

sum = 0    
for k, g in group.items():
    sum += g
print(group)
print(f"there are {sum} fish to start!")

# process just the first fish for now
# for i in range(80):
for i in range(256):
    spawn_count = 0
    for state, fish_count in group.items():
        if state == 0:
            spawn_count = fish_count
        else:
            group[state-1] = fish_count
            group[state] = 0
        
    if spawn_count != 0:
        group[8] = spawn_count
        group[6] += spawn_count
            
    sum = 0    
    for k, g in group.items():
        sum += g
    # print(group)
    print(f"there are now {sum} fishies after {i+1} days")
    logger.info(f",{i+1},{sum}")
