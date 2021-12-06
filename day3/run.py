import pandas as pd
from pathlib import Path

inputfile = Path(__file__).parent / 'input.csv'
data = pd.read_csv(inputfile, dtype=str)

print("****** PART 1 **********")

data = data['data'].apply(lambda x: pd.Series(list(x)))

for i in range(12):
    data[i] = data[i].astype(int)

print(data.dtypes)

gamma = []  # most common
epsilon = [] # least common
for i in range(12):
    sub = data[data[i] == 1][i]

    if len(sub) >= 500:
        gamma.append('1')
        epsilon.append('0')
    else:
        gamma.append('0')
        epsilon.append('1')


print(f"Gamma is {gamma}")
print(f"Epsilon is {epsilon}")

gamma = ''.join(gamma)
epsilon = ''.join(epsilon)
print(f"Gamma is {gamma}")
print(f"Epsilon is {epsilon}")

gamma = int(gamma)
epsilon = int(epsilon)
print(f"Gamma is {gamma}")
print(f"Epsilon is {epsilon}")
    
gamma = int(str(gamma),2)
epsilon = int(str(epsilon),2)
print(f"Gamma is {gamma}")
print(f"Epsilon is {epsilon}")

print(f"part 1: answer should be {gamma * epsilon}")

# co2 and oxygen!
print("********** PART 2 *********")
co2 = None  # most common
oxy = None # least common
sub0 = data.copy()
sub1 = data.copy()
for i in range(12):
    count0 = len(sub0)
    count1 = len(sub1)
    print(f"Iter {i}, Count0: {count0}, Count1: {count1}")
    if oxy is None and len(sub0) == 1:
        oxy = sub0.copy()

    if co2 is None and len(sub1) == 1:
        co2 = sub1.copy()
    
    print("BEFORE")
    print(sub1)
    # check the counts of the column for the 0s (least commons)
    sub0_0s = len(sub0[sub0[i] == 0])
    sub0_1s = len(sub0[sub0[i] == 1])
    print(f"Sub0: 0s - {sub0_0s}; 1s - {sub0_1s}")
    if sub0_0s < count0/2:
        # 0 is the least common, now propogate
        sub0 = sub0[sub0[i] == 0]
    elif sub0_1s < count0/2:
        # 1 is least common in the least, now propogate
        sub0 = sub0[sub0[i] == 1]
    else:
        print(f"Same {sub0_0s}=={sub0_1s} -- keeping the 0s")
        sub0 = sub0[sub0[i] == 0]

    # now check the most common
    sub1_0s = len(sub1[sub1[i] == 0])
    sub1_1s = len(sub1[sub1[i] == 1])
    print(f"Sub1: 0s - {sub1_0s}; 1s - {sub1_1s}")
    if sub1_0s > count1/2:
        # 0 is the most common, now propogate
        sub1 = sub1[sub1[i] == 0]
    elif sub1_1s > count1/2:
        # 1 is most common, now propogate
        sub1 = sub1[sub1[i] == 1]
    else:
        print(f"Same {sub1_0s}=={sub1_1s} -- keeping the 1s")
        sub1 = sub1[sub1[i] == 1]
        
    # check on the final size
    if oxy is None and i == 11:
        oxy = sub0.copy()

    if co2 is None and i == 11:
        co2 = sub1.copy()

oxy = ''.join([f"{x}" for x in oxy.values.tolist()[0]])
co2 = ''.join([f"{x}" for x in co2.values.tolist()[0]])

oxy = int(oxy,2)
co2 = int(co2,2)
print(oxy)
print(co2)

print(f"part 2: answer should be {oxy * co2}")

