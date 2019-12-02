import os
import functools
import itertools
import numpy as np

here = os.path.dirname(__file__)
input_path = os.path.join(here, 'input.txt')


def load_input():
    data = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append(line)
    return data


def load_board(board_strs):
    width = len(board_strs[0])
    height = len(board_strs)
    board = np.zeros((height, width), dtype=np.int8)
    for row,row_str in enumerate(board_strs):
        for col,str_value in enumerate(row_str):
            if str_value == '#':
                board[row, col] = 1
    return board


def board_sum(board):
    return sum(sum(board))


def iter_neighbors_indicies(board, row, col):
    start_row = max(0, row - 1)
    end_row = min(row + 2, board.shape[0])
    start_col = max(0, col - 1)
    end_col = min(col + 2, board.shape[1])
    for nr in range(start_row, end_row):
        for nc in range(start_col, end_col):
            if (nr,nc) == (row,col):
                continue
            yield nr,nc


def count_neighbors(board, row, col):
    total = 0
    for i in iter_neighbors_indicies(board, row, col):
        total += board[i]
    return total


def step_board(prev_board):
    new_board = np.zeros_like(prev_board)
    for row in range(new_board.shape[0]):
        for col in range(new_board.shape[1]):
            count = count_neighbors(prev_board, row, col)
            if count == 3:
                new_board[row, col] = 1
            elif prev_board[row, col] == 1 and count == 2:
                new_board[row, col] = 1
    return new_board


def main():
    board = load_board(load_input())
    corners = [(0,0), (0, board.shape[1] - 1), (board.shape[0] - 1, 0), (board.shape[0] - 1, board.shape[1] - 1)]
    for c in corners:
        board[c] = 1
    print(board)
    for i in range(100):
        board = step_board(board)
        for c in corners:
            board[c] = 1
        print('step', i)
        #print(board)
    print(board_sum(board))


if __name__ == "__main__":
    main()