import pandas as pd
from pathlib import Path

inputfile = Path(__file__).parent / 'input.csv'

boards = []
new_board = []
numbers = []
count = 0
with open(inputfile) as fp:
    lines = fp.readlines()
    for line in lines:
        count += 1
        if count == 1:
            numbers = [int(x) for x in line.strip().split(',')]
            continue

        if line.rstrip() == "":
            new_board = []
            # print('new board found')
            if new_board is not None:
                # print('saving old board')
                boards.append(new_board)
        else:
            new_board.append([int(x) for x in line.replace('  ', ' ').strip().split(' ')])
            

        
# print(numbers)
print(f"found {len(boards)}")
# print(boards)

# convert boards to pandas objects
pd_boards = []
for b in boards:
    pd_boards.append(pd.DataFrame(b))

def check_winner(board, numbers):
    # check each row
    for i, r in board.iterrows():
        if set(r.values.tolist()).issubset(set(numbers)): 
            print('winner on row!')
            return True

    for c in board.columns:
        if set(board[c].tolist()).issubset(set(numbers)):
            print('winner on column!')
            return True
    
    # print("No winner")
    return False

check_winner(pd_boards[0], [68,73])
check_winner(pd_boards[0], [68,73,98,51,49,91,90])
check_winner(pd_boards[0], [98,87,21,86,76])


print("****** PART 1 **********")

winning_board = None
for i in range(len(numbers)):
    # print(numbers[0:i+1])
    for b_i, b in enumerate(pd_boards):
        if check_winner(b, numbers[0:i+1]):
            print(f"yes on board {b_i} with numbers {numbers[0:i+1]}")
            winning_board = b
            break
    
    if winning_board is not None:
        break

print(i)
print(f"last number: {numbers[i]}")
print(winning_board)

# sum up the unmarked numbers
board_numbers = winning_board.unstack().to_frame().sort_index(level=1).T.values.tolist()[0]
for n in numbers[0:i+1]:
    if n in board_numbers:
        board_numbers.remove(n)

print(f"Final board numbers: {board_numbers}")
print(f"Final board sum: {sum(board_numbers)}")
print(f"Answer should be {sum(board_numbers) * numbers[i]}")

print("****** PART 2 **********")

last_board = None
board_winners = []
board_winner_id = None
last_numbers_called = None
for i in range(len(numbers)):
    # print(numbers[0:i+1])
    for b_i, b in enumerate(pd_boards):
        if b_i in board_winners:
            # print('Winner already declared for this board')
            continue
        
        if check_winner(b, numbers[0:i+1]):
            print(f"yes on board {b_i}")
            board_winners.append(b_i)
            last_board = b
            board_winner_id = b_i
            last_numbers_called = numbers[0:i+1]
    
print(f"Last board winner is {board_winner_id}")
print(last_board)
print(last_numbers_called)
print(last_numbers_called[-1])

board_numbers = last_board.unstack().to_frame().sort_index(level=1).T.values.tolist()[0]
for n in last_numbers_called:
    if n in board_numbers:
        board_numbers.remove(n)

print(f"Final board numbers: {board_numbers}")
print(f"Final board sum: {sum(board_numbers)}")
print(f"Answer should be {sum(board_numbers) * last_numbers_called[-1]}")

