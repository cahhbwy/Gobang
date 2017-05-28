#!/usr/bin/env python
# coding:utf-8


import numpy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="chessboard status file")
parser.add_argument("method", help="load, restart, play or help")
parser.add_argument("-x", help="player's x", type=int)
parser.add_argument("-y", help="player's y", type=int)
argv = parser.parse_args()

filename = argv.filepath
method = argv.method
user_x = -1
user_y = -1

board = ""
message = ""
ai_x = -1
ai_y = -1

if method not in ["load", "restart", "play", "help"]:
    message = "error"
    print message
    exit(1)

if method in ["load", "play", "help"]:
    with open(filename, "r") as f:
        board = f.readline()[:-1]
else:
    board = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    message = "continue"
    print message
    exit(0)

if method == "load":
    message = "continue"
    print message
    print board
    exit(0)

chess = numpy.array(map(lambda x: int(x) - 1, list(board))).astype(numpy.int32).reshape([15, 15])

if method == "play":
    if argv.x is not None and argv.y is not None:
        user_x = argv.x
        user_y = argv.y
    else:
        message = "error"
        print message
        print board
        print ai_x
        print ai_y
        exit(1)
    if user_x < 0 or user_x > 14 or user_y < 0 or user_y > 14 or chess[user_x, user_y] != 0:
        message = "wrong"
        print message
        print board
        print ai_x
        print ai_y
        exit(2)
    else:
        chess[user_x, user_y] = 1
        blank_x, blank_y = numpy.where(chess == 0)
        if blank_x.size == 0:
            message = "peace"
        else:
            rand_choice = numpy.random.randint(blank_x.size)
            ai_x, ai_y = blank_x[rand_choice], blank_y[rand_choice]
            chess[ai_x, ai_y] = -1
            message = "continue"
        board = chess.reshape(225) + 1
        board = ''.join(map(lambda x: str(x), board.tolist()))
        with open(filename, "w") as f:
            f.write(board + "\n")
        print message
        print board
        print ai_x
        print ai_y
else:
    x = 7
    y = 7
    message = "help"
    print message
    print x
    print y
