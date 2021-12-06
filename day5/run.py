import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt



inputfile = Path(__file__).parent / 'input.csv'

lines = []
board = []
min_x = None
max_x = None
min_y = None
max_y = None

def determine_points(xy1, xy2):
    points = []
    print(f"{xy1} -> {xy2}")

    if xy1[0] == xy2[0]:
        # vertical
        start = None
        end = None
        if xy1[1] > xy2[1]:
            start = xy2[1]
            end = xy1[1]
        else:
            start = xy1[1]
            end = xy2[1]
            
        for p in range(start, end+1):
            points.append([xy1[0], p])
    elif xy1[1] == xy2[1]:
        # horizontal line
        start = None
        end = None
        if xy1[0] > xy2[0]:
            start = xy2[0]
            end = xy1[0]
        else:
            start = xy1[0]
            end = xy2[0]
            
        for p in range(start, end+1):
            points.append([p, xy1[1]])
    else: 
        # diagonal
        # calculate the steps
        x_step = xy2[0] - xy1[0]
        y_step = xy2[1] - xy1[1]
        if abs(x_step) != abs(y_step):
            raise Exception("steps in x and y should be the same")

        start_x = None
        if x_step < 0:
            step_x_by = -1
        else:
            step_x_by = 1

        if y_step < 0:
            step_y_by = -1
        else:
            step_y_by = 1

        start_x = xy1[0]
        start_y = xy1[1]
        
        for p in range(abs(x_step)+1):
            points.append([start_x + step_x_by * p, start_y + step_y_by * p])
    
    return points

print("testing determine points")
p_s = determine_points([2,2], [10,2])
for p in p_s:
    print(p)

p_s = determine_points([10,2], [2,2])
for p in p_s:
    print(p)

print("vertical")
p_s = determine_points([10,12], [10,20])
for p in p_s:
    print(p)

p_s = determine_points([10,20], [10,12])
for p in p_s:
    print(p)


print("diagonal")
p_s = determine_points([2,2], [10,10])
for p in p_s:
    print(p)

p_s = determine_points([10,10], [2,2])
for p in p_s:
    print(p)

# 9,7 -> 7,9
p_s = determine_points([9,7], [7,9])
for p in p_s:
    print(p)

with open(inputfile) as fp:
    read_lines = fp.readlines()
    for line in read_lines:
        if line is not None:
            line = line.strip()
        
        l, r = line.split(' -> ')
        l1, l2 = l.split(',')
        r1, r2 = r.split(',')

        # convert all data to integers (inefficiently)
        l1 = int(l1)
        l2 = int(l2)
        r1 = int(r1)
        r2 = int(r2)
    
        # part 1
        # only add lines where l1 = r1 or l2 = r2
        # if l1 == r1 or l2 == r2:
            # lines.append([[l1,l2], [r1, r2]])

        # Part 2 use the following
        lines.append([[l1,l2], [r1, r2]])
    
    x_s = []
    y_s = []
    for line in lines:
        x_s.append(line[0][0])
        x_s.append(line[1][0])
        y_s.append(line[0][1])
        y_s.append(line[1][1])
    
# print(lines)

min_x = min(x_s)
max_x = max(x_s)
min_y = min(y_s)
max_y = max(y_s)

print(f"X's min_x: {min_x}, max_x: {max_x}")
print(f"Y's min_y: {min_y}, max_y: {max_y}")

print("****** PART 1 and 2 **********")

table = pd.DataFrame(np.zeros((1000, 1000), dtype=int))

print(table)

# set the value in the table - values are backwards, y,x in table.at
count = 0
for line in lines:
    count += 1
    # print(f"{line[0][0]} -> {line[1][0]}")
    p_s = determine_points(line[0], line[1])

    # should we sort if we are on a diagonal?
    for p in p_s:
        table.at[p[1], p[0]] += 1

    # if count >= 4:
        # break
        
# get any value > 1
print(table.head(10))
count = 0
for c in table.columns:
    column = table[c]
    count += column[column > 1].count() 
print(f"number of values greater than 1: {count}")



# plt.scatter(x, y)
# plt.xlim(0,10)
# plt.ylim(0,10)
# plt.show()

