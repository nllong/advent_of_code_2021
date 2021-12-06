import pandas as pd
from pathlib import Path

inputfile = Path(__file__).parent / 'input.csv'
data = pd.read_csv(inputfile)

# 1 reading
res1 = data['data'].diff()

# 3 readings
res3 = data['data'].diff(3)

print(f"Number of increases (1 int): {len(res1.loc[res1 > 0])}")
print(f"Number of increases (3 int): {len(res3.loc[res3 > 0])}")

