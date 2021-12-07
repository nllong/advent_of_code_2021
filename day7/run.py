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

logging.info("Day 7 - crabs")
logger = logging.getLogger('day7')

inputfile = Path(__file__).parent / 'input.csv'

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
            for crab in line.split(','):
                data.append(int(crab))

# find the middle number
# print(data)
all_data = np.array(data)

print("*** part 1 ***")
middle = np.median(all_data)
print(f"Median is {middle}")

total_fuel = 0
for crab in all_data:
    total_fuel += abs(crab - middle)

print(f"Will take {total_fuel} to get all the crabs to the optimal place")

print("*** part 2 ***")
average = np.mean(all_data)
print(f"Average before rounding {average}")
average = int(round(average, 0))
print(f"Average after rounding {average}")

# test around the average +/- 5
guesses = []
for average in [x for x in range(average-5, average+5, 1)]:
    total_fuel = 0
    for crab in all_data:
        
        steps = abs(crab - average)
        fuel = sum([x for x in range(steps+1)])
        
        print(f"Crab is at {crab} and going to {average}, which is {steps} steps, total fuel for crap {fuel}")

        total_fuel += fuel

    guesses.append(total_fuel)

# the value is going to be around the average, so just take the minimum of the guesses.
print(f"Part 2: Will take {min(guesses)} to get all the crabs to the optimal place")
