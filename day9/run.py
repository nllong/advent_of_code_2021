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
day = 'Day 9'
logging.info(f"{day} - smoke low point")
logger = logging.getLogger(day)

# inputfile = Path(__file__).parent / 'input_sample.csv'
inputfile = Path(__file__).parent / 'input.csv'

data = []
data = pd.read_csv(inputfile, header=None, dtype=str)
data = data[0].apply(lambda x: pd.Series(list(x)))
data = data.astype(int)


# plt.contour(range(0,10), range(0,5), Z, colors='black');
print(data)

def find_adjancent(data, x, y):
    left = None
    right = None
    up = None
    down = None

    if x > 0:
        left = data.at[y, x-1]
    if y > 0:
        up = data.at[y-1, x]
    if x < data.shape[1] -1:
        right = data.at[y, x+1]
    if y < data.shape[0] - 1:
        down = data.at[y+1, x]

    return [left, up, right, down]
    
def am_i_min(value, adjacency):
    if all(value < x for x in list(filter(partial(is_not, None), adjacency))):
        print(f'yep, i am small, adj was {list(filter(partial(is_not, None), adjacency))}')
        return True
    else:
        return False

minimums = []
count = 0
for x in range(0, data.shape[1]):
    for y in range(0, data.shape[0]):
        count += 1

        print(f"Checking for data at [{x},{y}] which has value {data.at[y,x]}")
        adj = find_adjancent(data, x, y)
        if am_i_min(data.at[y,x], adj):
            minimums.append([x, y, data.at[y,x]])
        
answer = 0
for minimum in minimums:
    answer += minimum[2] + 1
print(f"Part 1 {answer}")

print(" ***** Part 2 *****")

def go_all_directions(data, x, y):
    """Go forth in all directions and return the basins"""
    values = []

    # go left until 9 or None
    print("Going left!")
    if adj[0]:
        for x_2 in range(x, -1, -1):
            if data.at[y, x_2] != 9 and data.at[y, x_2] is not None:
                v = [x_2, y, data.at[y, x_2]]
                if v not in values:
                    values.append(v)
            
            adj_2 = find_adjancent(data, x_2, y)
            print(f"Looking left for basin at [{x_2}, {y}], which has adj of {adj_2}")
            if adj_2[0] == 9 or adj_2[0] is None:
                break   
    
    # go right until 9 or None
    print("Going right!")
    if adj[2]:
        for x_2 in range(x, data.shape[1]):
            if data.at[y, x_2] != 9 and data.at[y, x_2] is not None:
                v = [x_2, y, data.at[y, x_2]]
                if v not in values:
                    values.append(v)
            
            adj_2 = find_adjancent(data, x_2, y)
            print(f"Looking right for basin at [{x_2}, {y}], which has adj of {adj_2}")
            if adj_2[2] == 9 or adj_2[2] is None:
                break
            
    # go up until 9 or None
    print("Going up!")
    if adj[1]:
        for y_2 in range(y, -1, -1):
            if data.at[y_2, x] != 9 and data.at[y_2, x] is not None:
                v = [x, y_2, data.at[y_2, x]]
                if v not in values:
                    values.append(v)
            
            adj_2 = find_adjancent(data, x, y_2)
            print(f"Looking up for basin at [{x}, {y_2}], which has adj of {adj_2}")
            if adj_2[1] == 9 or adj_2[1] is None:
                break

    # go up until 9 or None
    print("Going down!")
    if adj[3]:
        for y_2 in range(y, data.shape[0]):
            if data.at[y_2, x] != 9 and data.at[y_2, x] is not None:
                v = [x, y_2, data.at[y_2, x]]
                if v not in values:
                    values.append(v)

            adj_2 = find_adjancent(data, x, y_2)
            print(f"Looking down for basin at [{x}, {y_2}], which has adj of {adj_2}")
            if adj_2[3] == 9 or adj_2[3] is None:
                break
    
    return values

# find all the low points around the minimums
basins = []
for minimum in minimums:
    new_basin = []
    x = minimum[0]
    y = minimum[1]
    z = minimum[2]
    
    adj = find_adjancent(data, x, y)
    print(f"Checking for data at [{x},{y}] which has value {data.at[y,x]}")
    print(f"Point has the following adj {adj}")
    # add current point to the basin
    new_basin.append([x, y, data.at[y, x]])

    new_x = x
    new_y = y
    count = 0
  
    # now go all the directions again until there are no new directions to go
    key = '_'.join([str(new_x), str(new_y)])
    stepped = {
        key: [new_x, new_y, data.at[new_y, new_x], False]
    }
    
    while any([x[3] == False for x in stepped.values()]):
        add_stepped = {}
        for key, step in stepped.items():
            print(f"looking around {step}")
            directions = go_all_directions(data, step[0], step[1])
            
            # after we step then flip the bit
            # key = '_'.join([str(step[0]), str(step[1])])
            stepped[key] = [step[0], step[1], data.at[step[1], step[0]], True]

            if [step[0], step[1], step[2]] not in new_basin:
                new_basin.append([step[0], step[1], step[2]])

            # add in the steps to the other directions
            for dir in directions:
                print(f'checking other directions {dir}')
                key = '_'.join([str(dir[0]), str(dir[1])])
                if key not in stepped.keys():
                    add_stepped[key] = [dir[0], dir[1], data.at[dir[1], dir[0]], False]  
                
        stepped.update(add_stepped)
        print(f"The stepped hash is {stepped}")
        
    print(f"Basin is {new_basin}")
    print("\n")
    basins.append(new_basin)

# All the basins  -- find the largest
                # index, length
largest_indexes = [[0,0], [0,0], [0,0]]

for index, b in enumerate(basins):
    print(f"Basin {b[0]} has {len(b)} points. All {b}")

    if len(b) > largest_indexes[0][1]:
        largest_indexes[0] = [index, len(b)]
    elif len(b) > largest_indexes[1][1]:
        largest_indexes[1] = [index, len(b)]
    elif len(b) > largest_indexes[2][1]:
        largest_indexes[2] = [index, len(b)]

print(largest_indexes)
print(f"the answer should be {largest_indexes[0][1] * largest_indexes[1][1] * largest_indexes[2][1]}")
    

# convert the data to XY list of list for plotting
to_plot = data.values.tolist()
plt.contourf(range(0,data.shape[1]), range(0,data.shape[0]), to_plot, 100, cmap='RdGy')
plt.colorbar()
plt.show()

