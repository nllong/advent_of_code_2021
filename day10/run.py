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
day = 'Day 10'
logging.info(f"{day} - parens")
logger = logging.getLogger(day)

# inputfile = Path(__file__).parent / 'input_sample.csv'
inputfile = Path(__file__).parent / 'input.csv'

data = []
ln_count = 0
with open(inputfile) as fp:
    read_lines = fp.readlines()
    for line in read_lines:
        ln_count += 1
        if line is not None:
            line = line.strip()

            data.append(line)
            
# Python3 code to Check for 
# balanced parentheses in an expression
open_list = ["[","{","(","<"]
close_list = ["]","}",")",">"]

inverses = dict(zip(open_list, close_list))
cost = {
    "]": 57,
    "}": 1197,
    ")": 3,
    ">": 25137
}

def check(my_string):
    queue = []
    for index, char in enumerate(my_string):
        if len(queue) == 0:
            queue.append(char)
            continue
        elif char not in open_list + close_list:
            raise Exception(f'Found invalid character at index {index} of {char}')
        else:
            # enqueue if opening
            if char in open_list:
                queue.append(char)
                if index == len(my_string) -1:
                    print('DOH, at end and added a new value')
                    return 'incomplete', char, f"Expected {inverses[popped]} but found {char}", queue
                else:
                    continue
            else:
                # try to dequeue the next value
                popped = queue.pop()
                # print(f"Found closing char of {char} and popped {popped}")
                if char == inverses[popped]:
                    # all is good
                    print(f"checking lengths {index} :: {len(my_string)-1}")
                    if index == len(my_string)-1:
                        print("SWWEEETTT and done with the list!")
                        if len(queue) == 0:
                            print("line was complete")
                        else:
                            print(f"line was incomplete {queue}")
                            return 'incomplete', char, f"Expected {inverses[popped]} but found {char}", queue       
                else:
                    return 'matching error', char, f"Expected {inverses[popped]} but found {char}", None
    
    return 'matches', None, None, None

total_cost = 0
data_part_2 = []
for index, string in enumerate(data):
    print(f"checking {index} with {string}")
    err_type, illegal_char, message, remaining_queue = check(string)
    if err_type == 'matches':
        print(f"{index} of string {string} is valid")
    elif err_type == 'incomplete':
        print(f"{index} of string {string} is incomplete")
        data_part_2.append([string, remaining_queue]) 
    elif err_type == 'matching error':
        total_cost += cost[illegal_char]
        print(f"{index} has s {string} and checks with {message}")  
    else:
        raise Exception(f"Found unknown error type of {err_type}")
    print("\n")
print(f"Part 1 -- Total cost is {total_cost}")

print(f"Part 2 -- Incomplete lines")
cost_2 = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

total_scores = []
for d in data_part_2:
    print(f"Processing string {d[0]} with remaining queue of {d[1]}")
    # reverse remaining queue
    d[1].reverse()
    score = 0
    for index, missing in enumerate(d[1]):
        print(f"Missing {missing} which costs {cost_2[missing]} current score {score}")
        score = (5 * score) + cost_2[missing]
        print(f"Score after = {score}")

    total_scores.append(score)

print(f"total score: {total_scores}")
print(f"median score is {np.median(np.array(total_scores))}")
