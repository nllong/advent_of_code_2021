import pandas as pd

data = pd.read_csv('input_all.csv')

res = data['data'].diff(3)

print(res)
print(f"Number of increases {len(res.loc[res > 0])}")

