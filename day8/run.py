import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import itertools

import logging

# create file handler which logs even debug messages
logging.basicConfig(filename=Path(__file__).parent / 'output.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
day = 'Day 8'
logging.info(f"{day} - seven segment display")
logger = logging.getLogger(day)

# inputfile = Path(__file__).parent / 'input_sample.csv'
inputfile = Path(__file__).parent / 'input.csv'

# 0 = 6 segments *****
# 1 = 2 segments
# 2 = 5 segments  ***
# 3 = 5 segments  ***
# 4 = 4 segments
# 5 = 5 segments  ***
# 6 = 6 segments *****
# 7 = 3 segments
# 8 = 7 segements
# 9 = 6 segments *****

data = []
displayed = []
signals = []
ln_count = 0
with open(inputfile) as fp:
    read_lines = fp.readlines()
    for line in read_lines:
        ln_count += 1
        if line is not None:
            line = line.strip()

            l, r = line.split('|')
            signals.append([''.join(sorted(x.strip())) for x in l.strip().split(' ')])
            displayed.append([x.strip() for x in r.strip().split(' ')])

group = {
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
}

# group them into the number of digits -- flatten
for display in list(itertools.chain(*displayed)):
    group[len(display)].append(display)

total_part_1 = 0
for i, g in group.items():
    print(f"{i} segments have {len(g)} items")
    if i in [2, 3, 4, 7]:
        total_part_1 += len(g)

print(f"Part 1 with 2, 3, 4, 7 segments is {total_part_1} ")


# now figure out which segments are which letters
#  0000
# 1    2
# 1    2
#  3333
# 4    5
# 4    5
#  6666

# go through the signals and deduce - singals are already sorted
deductions = []

for s_s in signals:
    full_deduction = False
    mappings = {
        "a": None,
        "b": None,
        "c": None,
        "d": None,
        "e": None,
        "f": None,
        "g": None,
    }
    # group the numbers first
    group = {
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
    }
    for s in s_s:
        group[len(s)].append(s)

    while full_deduction is False:
        # verify that we have a number in each
        if all([len(x) > 0 for x in group.values()]):
            pass
            # print('yes we have all!')
        else:
            raise Exception("hmm, I can't deduce if I don't have all the segment signals")

        # determine the segment 0 -- which is the value that is not between 
        # digit 7 (3 segments) and digit 1 (2 segments)
        diff = list(set(sorted(group[3][0])).difference(set(sorted(group[2][0]))))
        print(f"Segment 0 is {diff[0]}")
        mappings[diff[0]] = 0

        # determine the segment 2 and segment 5
        for d in group[6]:
            small_list = [char for char in group[2][0]]  # this is the digit 1
            large_list = [char for char in d]            # this is digit 0, 6, or 9
            
            if all(elem in large_list for elem in small_list):
                print(f'Nope, must be a 0 or 9 {d}')
            else:
                print(f'Yep, must be a 6')
                print(f'The digit 1 is segments {small_list}')
                print(f'The digit with 6 segments {large_list}')

                # the digit from 1 that is in digit 6 is segment 5
                value = list(set(small_list) & set(large_list))[0]
                print(f"Found segment 5 is: {value}")
                mappings[value] = 5

                # the digit 1 that is not from above is segment 2
                value = list(set(list(value)).symmetric_difference(set(group[2][0])))[0]
                print(f"Found segment 2 is: {value}")
                mappings[value] = 2 
                continue
            
        # determine segment 1 by intersecting digit 4 and 0 and removing known mappings
        dig_4 = group[4][0]
        seg_6s = group[6]

        # get my known mappings
        knowns = []
        for letter, number in mappings.items():
            if number is not None:
                knowns.append(letter)
        print(f"here are my known mappings: {knowns}")
        
        for d in seg_6s:
            small_list = sorted([char for char in dig_4])
            large_list = sorted([char for char in d]) 
            print(f"my seg_6s could be {large_list}")

            values = sorted(list(set(small_list) & set(large_list)))
            print(f"After intersecting with dig 4 {values}")
            
            # now exclude knowns
            values = list(set(values).difference(set(knowns))) 
            print(f"new values after removing knowns {values}")
            if len(values) == 1:
                print(f"NEW VALUE FOUND for segment 1 of {values[0]}")
                mappings[values[0]] = 1
                continue
            
        # now find segment 3 by just diffing the known mappings
        knowns = []
        for letter, number in mappings.items():
            if number is not None:
                knowns.append(letter)
        print(f"here are my known mappings: {knowns}")

        dig_4 = [char for char in group[4][0]]
        values = sorted(list(set(dig_4).difference(set(knowns))))
        print(f"new values after removing knowns {values}")
        if len(values) == 1:
            print("NEW VALUE FOUND for segment 3!!!")
            mappings[values[0]] = 3

        # now find segment 6 by looking at 6 segments again
        seg_6s = group[6]
        knowns = []
        for letter, number in mappings.items():
            if number is not None:
                knowns.append(letter)
        print(f"here are my known mappings: {knowns}")

        for d in seg_6s:
            large_list = sorted([char for char in d]) 
            print(f"my seg_6s could be {large_list}")

            values = sorted(list(set(large_list).difference(set(knowns))))
            print(f"After intersecting with dig 4 {values}")
            if len(values) == 1:
                print(f"NEW VALUE FOUND for segment 6 of {values[0]}")
                mappings[values[0]] = 6
                continue

        # now the last one seg 4 - just the last unknown
        for letter, value in mappings.items():
            if value is None:
                mappings[letter] = 4
                         
        print(mappings)

        # check if full deduction
        if all([x is not None for x in mappings.values()]):
            full_deduction = True
            print("done with deductions")
            print(mappings)
        else:
            print('still deducing')

    deductions.append(mappings)

print(deductions)
print(len(deductions))

segment_mappings = {
    "012456": 0,
    "25": 1,
    "02346": 2,
    "02356": 3,
    "1235": 4,
    "01356": 5,
    "013456": 6,
    "025": 7,
    "0123456": 8,
    "012356": 9
}        

all_values = []
for index, display in enumerate(displayed):
    print(f"Finding {index} for {display}")
    mappings = deductions[index]
    back_to_number = []
    for value in display:
        answer = []
        for char in value:
            answer.append(mappings[char])
        
        # convert to string
        answer_concat = "".join([f"{x}" for x in sorted(answer)])
        print(answer_concat)
        back_to_number.append(segment_mappings[answer_concat])
            
 
    print(back_to_number)
    all_values.append(int(''.join([f"{n}" for n in back_to_number])))

print(all_values)
print(f"dear god answer part 2 is {sum(all_values)}")
        




