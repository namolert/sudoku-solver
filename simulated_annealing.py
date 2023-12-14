import numpy as np
import time


def print_board(board):
    for i in range(len(board)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(board[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(board[i, j]) + " "
        print(line)


def calculate_temp(board):
    record = []
    for i in range(200):
        record.append(get_cost(generate_start_board(board)))
    return np.std(record)


# get position that needed to fill the number
def get_zero_pos(board):
    zero_pos = dict()
    zero_pos_2 = []
    counter = 1

    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            for i in range(3):
                for j in range(3):
                    if board[row + i][col + j] == 0:
                        if counter not in zero_pos:
                            zero_pos[counter] = [(row + i, col + j)]
                        else:
                            zero_pos[counter].append((row + i, col + j))

                        zero_pos_2.append((row + i, col + j))
            counter += 1

    return zero_pos, zero_pos_2


# insert number in to zero position
def generate_start_board(board):
    start_board = board.copy()
    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            nums_set = set()
            for i in range(3):
                for j in range(3):
                    if start_board[row + i][col + j] != 0:
                        nums_set.add(start_board[row + i][col + j])
            for i in range(3):
                for j in range(3):
                    if start_board[row + i][col + j] == 0:
                        number = np.random.choice(
                            [i for i in range(1, 10) if i not in nums_set]
                        )
                        start_board[row + i][col + j] = number
                        nums_set.add(number)

    return start_board


# get random square and swap 2 positions
def generate_new_board(board, zero_pos, gen_count, temp, zero_pos_2):
    selected_board = board.copy()
    selected_board_cost = get_cost(board)
    node_used = 0

    for i in range(gen_count):
        new_board = board.copy()
        node_used += 1

        index = np.random.randint(1, 9)
        while zero_pos.get(index) == None or len(zero_pos[index]) < 2:
            index = np.random.randint(1, 9)

        idx1, idx2 = np.random.choice(len(zero_pos_2), 2, replace=False)
        pos1, pos2 = zero_pos_2[idx1], zero_pos_2[idx2]

        new_board[pos1[0]][pos1[1]], new_board[pos2[0]][pos2[1]] = (
            new_board[pos2[0]][pos2[1]],
            new_board[pos1[0]][pos1[1]],
        )

        selected_board, selected_board_cost = choose_board(
            selected_board, new_board, temp
        )

        if selected_board_cost == 0:
            return selected_board, selected_board_cost, node_used

    return selected_board, selected_board_cost, node_used


# choose between current board and new board
def choose_board(current_board, new_board, temp):
    current_board_cost = get_cost(current_board)
    new_board_cost = get_cost(new_board)

    if new_board_cost == 0:
        return new_board, new_board_cost

    dif = new_board_cost - current_board_cost

    if dif < 0:
        return new_board, new_board_cost
    elif np.random.uniform(1, 0, 1) < np.exp(-dif / temp):
        return new_board, new_board_cost
    else:
        return current_board, current_board_cost


# calculate cost function
def get_cost(board):
    cost = 0

    for row in board:
        cost += 9 - len(np.unique(row))

    board_t = np.transpose(board)
    for row_t in board_t:
        cost += 9 - len(np.unique(row_t))

    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            is_valid = True
            nums_set = set()
            for i in range(3):
                if not is_valid:
                    break
                for j in range(3):
                    if not is_valid:
                        break
                    if board[row + i][col + j] in nums_set:
                        cost += 1
                        is_valid = False
                    else:
                        nums_set.add(board[row + i][col + j])

    return cost


board = np.array(
    [
        [5, 0, 0, 4, 6, 7, 3, 0, 9],
        [9, 0, 3, 8, 1, 0, 4, 2, 7],
        [1, 7, 4, 2, 0, 3, 0, 0, 0],
        [2, 3, 1, 9, 7, 6, 8, 5, 4],
        [8, 5, 7, 1, 2, 4, 0, 9, 0],
        [4, 9, 6, 3, 0, 8, 1, 7, 2],
        [0, 0, 0, 0, 8, 9, 2, 6, 0],
        [7, 8, 2, 6, 4, 1, 0, 0, 5],
        [0, 1, 0, 0, 0, 0, 7, 0, 8],
    ]
)

# board = np.array(
#     [
#         [0, 9, 8, 1, 0, 0, 2, 0, 4],
#         [0, 0, 2, 0, 0, 0, 0, 8, 0],
#         [0, 0, 0, 0, 4, 0, 0, 6, 0],
#         [0, 0, 6, 0, 1, 0, 5, 0, 7],
#         [0, 0, 0, 0, 0, 0, 0, 4, 0],
#         [3, 0, 0, 9, 0, 0, 0, 0, 0],
#         [0, 0, 5, 0, 7, 0, 1, 0, 2],
#         [0, 6, 0, 0, 0, 5, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 8, 0, 0],
#     ]
# )


def solve(board):
    start_time = time.time()
    temp = calculate_temp(board)
    cool_down_rate = 0.99

    zero_pos, zero_pos_2 = get_zero_pos(board)

    board = generate_start_board(board)
    board_cost = get_cost(board)

    attempt = 0
    count = 0
    node_used = 1

    while board_cost > 0:
        new_board, new_board_cost, nodes = generate_new_board(
            board, zero_pos, 30, temp, zero_pos_2
        )

        node_used += nodes

        if new_board_cost >= board_cost:
            attempt += 1
        else:
            attempt = 0

        board, board_cost = new_board, new_board_cost
        temp *= cool_down_rate
        count += 1

        if board_cost == 0:
            break

        if attempt > 100:
            temp += 2

        if node_used >= 1000000:
            break

    if node_used >= 1000000:
        print("Cannot find a solution.")
    else:
        print_board(board)
    end_time = time.time()

    print(f"Time Used: {end_time - start_time} seconds.")
    print(f"Node Created: {node_used} times.")


solve(board)
