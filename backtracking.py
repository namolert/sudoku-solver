import datetime
import tracemalloc
import numpy as np

board_easy = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]
board_med = [
    [2,0,0,5,0,7,4,0,6],
    [0,0,0,0,3,1,0,0,0],
    [0,0,0,0,0,0,2,3,0],
    [0,0,0,0,2,0,0,0,0],
    [8,6,0,3,1,0,0,0,0],
    [0,4,5,0,0,0,0,0,0],
    [0,0,9,0,0,0,7,0,0],
    [0,0,6,9,5,0,0,0,2],
    [0,0,1,0,0,6,0,0,8]
]
board_hard = [
    [0,9,8,1,0,0,2,0,4],
    [0,0,2,0,0,0,0,8,0],
    [0,0,0,0,4,0,0,6,0],
    [0,0,6,0,1,0,5,0,7],
    [0,0,0,0,0,0,0,4,0],
    [3,0,0,9,0,0,0,0,0],
    [0,0,5,0,7,0,1,0,2],
    [0,6,0,0,0,5,0,0,0],
    [0,0,0,0,0,0,8,0,0]
]
board_ex = [
    [5,0,0,4,6,7,3,0,9],
    [9,0,3,8,1,0,4,2,7],
    [1,7,4,2,0,3,0,0,0],
    [2,3,1,9,7,6,8,5,4],
    [8,5,7,1,2,4,0,9,0],
    [4,9,6,3,0,8,1,7,2],
    [0,0,0,0,8,9,2,6,0],
    [7,8,2,6,4,1,0,0,5],
    [0,1,0,0,0,0,7,0,8]
]


node_count = 0
current_memories = []
peak_memories = []

def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None


def solve(board):
    # Node count
    global node_count
    node_count += 1

    # Meromy usage count
    global current_memories
    global peak_memories
    current, peak = tracemalloc.get_traced_memory()
    current_memories.append(current/(1024*1024))
    peak_memories.append(peak/(1024*1024))
    tracemalloc.reset_peak()
    del current, peak

    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False


def app(board):
    # Print board before solve  
    print_board(board)

    tracemalloc.start()

    start_time = datetime.datetime.now()
    solve(board)
    end_time = datetime.datetime.now()

    # Print board after solve 
    print("________________________\n")
    print_board(board)

    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")
    print(f"Node Created: {node_count} times")
    print(f"Average Current Memory: {round(np.mean(current_memories), 6)} MB")
    print(f"Average Peak Memory: {round(np.mean(peak_memories), 6)} MB")

# app(board_easy)
# app(board_med)
app(board_hard)
# app(board_ex)