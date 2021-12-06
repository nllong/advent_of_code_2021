import pandas as pd
from pathlib import Path

inputfile = Path(__file__).parent / 'input.csv'
data = pd.read_csv(inputfile)

state = {
    'horizontal': 0,
    'vertical': 0,
    'aim': 0,
}
# iterate through data
for d in data['data']:
    action, value = d.split(' ')
    value = int(value)

    print(f"{action}, {value}")
    if action == 'forward':
        state['horizontal'] += value
        
        new_vert = state['aim'] * value
        state['vertical'] += new_vert
    elif action == 'down':
        state['aim'] += value
        # state['vertical'] += value
    elif action == 'up':
        state['aim'] -= value
        # state['vertical'] -= value
    else:
        raise Exception(f'Unknown direction {action}')



    


print(f"final horizontal, vertical, mult: {state['horizontal']}, {state['vertical']}, {state['horizontal'] * state['vertical']}")

