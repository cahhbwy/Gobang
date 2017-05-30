#!/usr/bin/env python
# coding:utf-8

import numpy

kinds = {
    0: [
        '.oooo.x',
        'boooo.x',
        'xo.ooox',
        'xoo.oox'
    ],
    2: [
        'x.ooo.x',
        '.o.oo.x',
        '.oo.o.x'
    ],
    4: [
        'booo..x',
        'boo.o.x',
        'bo.oo.x'
    ],
    6: [
        'x.oo..x',
        'x.o.o.x',
    ],
    8: [
        'boo...x',
        'bo.o..x',
        'bo..o.x',
        'bo...ox'
    ],
    10: [
        'xo....x',
        'x.o...x',
        'x..o..x'
    ],
    12: [
        'bo....x',
        'b.o...x',
        'b..o..x',
        'b...o.x',
        'b....ox'
    ]
}


def match(code, mode):
    if len(code) != len(mode):
        return False
    else:
        for i, j in zip(code, mode):
            if j != 'x' and i != j:
                return False
        else:
            return True


def value_one(code):
    code_r = code[::-1]
    for v, kind in kinds.items():
        for k in kind:
            if match(code, k) or match(code_r, k):
                return 4096 >> v
    else:
        return 0


def encode(value, player=-1):
    return ''.join(['o' if v == player else '.' if v == 0 else 'b' for v in value])


class Gobang:
    def __init__(self, size=15, user_first=True):
        self.size = size
        self.user_first = True
        self.board = numpy.zeros((size + 2, size + 2)).astype(numpy.int32) + 2
        self.board[1:self.size + 1, 1:self.size + 1] = 0

    def save(self, filename="status.board"):
        board = self.board[1:self.size + 1, 1:self.size + 1].reshape(self.size * self.size) + 1
        board = ''.join(map(lambda x: str(x), board.tolist()))
        with open(filename, 'w') as f:
            f.write(board + "\n")

    def load(self, filename="status.board"):
        with open(filename, 'r') as f:
            board = f.readline()[:-1]
            self.board[1:self.size + 1, 1:self.size + 1] = numpy.array(map(lambda x: int(x) - 1, list(board))).astype(numpy.int32).reshape([self.size, self.size])

    def value(self, player=-1):
        size = self.size + 2
        value_1 = numpy.zeros((self.size, self.size)).astype(numpy.uint32)
        value_2 = numpy.zeros((self.size, self.size)).astype(numpy.uint32)
        # 左-右
        for i in range(1, self.size + 1):
            for j in range(size - 6):
                if i == 8 and j == 5:
                    pass
                index = [numpy.array([i] * 7), numpy.arange(j, j + 7)]
                v = self.board[index[0], index[1]].tolist()
                index = [index[0][1:6] - 1, index[1][1:6] - 1]
                c = encode(v, player)
                value_1[index[0], index[1]] += value_one(c)
                c = encode(v, -player)
                value_2[index[0], index[1]] += value_one(c)
        # 上-下
        for j in range(1, self.size + 1):
            for i in range(size - 6):
                index = [numpy.arange(i, i + 7), numpy.array([j] * 7)]
                v = self.board[index[0], index[1]].tolist()
                index = [index[0][1:6] - 1, index[1][1:6] - 1]
                c = encode(v, player)
                value_1[index[0], index[1]] += value_one(c)
                c = encode(v, -player)
                value_2[index[0], index[1]] += value_one(c)
        # 左上-右下
        for i in range(size - 6):
            for j in range(size - 6):
                index = [numpy.arange(i, i + 7), numpy.arange(j, j + 7)]
                v = self.board[index[0], index[1]].tolist()
                index = [index[0][1:6] - 1, index[1][1:6] - 1]
                c = encode(v, player)
                value_1[index[0], index[1]] += value_one(c)
                c = encode(v, -player)
                value_2[index[0], index[1]] += value_one(c)
        # 左下-右上
        for i in range(6, size - 1):
            for j in range(size - 6):
                index = [numpy.arange(i, i - 7, -1), numpy.arange(j, j + 7)]
                v = self.board[index[0], index[1]].tolist()
                index = [index[0][1:6] - 1, index[1][1:6] - 1]
                c = encode(v, player)
                value_1[index[0], index[1]] += value_one(c)
                c = encode(v, -player)
                value_2[index[0], index[1]] += value_one(c)
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i + 1, j + 1] == 0:
                    value_1[i, j] += 128 - numpy.floor(numpy.sqrt((i - self.size / 2) ** 2 + (j - self.size / 2) ** 2))
                    value_2[i, j] += 128 - numpy.floor(numpy.sqrt((i - self.size / 2) ** 2 + (j - self.size / 2) ** 2))
                else:
                    value_1[i, j] = value_2[i, j] = 0
        max_1 = numpy.max(value_1)
        max_2 = numpy.max(value_2)
        argmax_1 = numpy.where(value_1 == max_1)
        argmax_2 = numpy.where(value_2 == max_2)
        if max_1 * 1.5 >= max_2:
            choice = numpy.random.randint(argmax_1[0].size)
            return argmax_1[0][choice], argmax_1[1][choice]
        else:
            choice = numpy.random.randint(argmax_2[0].size)
            return argmax_2[0][choice], argmax_2[1][choice]

    def input(self, i, j, player=1):
        if 0 <= i < self.size + 2 and 0 <= j < self.size + 2:
            if self.board[i, j] == 0:
                self.board[i, j] = player
                return True
            else:
                return False
        else:
            return False

    def win(self, i, j, player=-1):
        i1 = i2 = i
        j1 = j2 = j
        while self.board[i1][j] == player:
            i1 -= 1
        while self.board[i2][j] == player:
            i2 += 1
        if i2 - i1 > 5:
            return True
        while self.board[i][j1] == player:
            j1 -= 1
        while self.board[i][j2] == player:
            j2 += 1
        if j2 - j1 > 5:
            return True
        i1 = i2 = i
        j1 = j2 = j
        while self.board[i1][j1] == player:
            i1 -= 1
            j1 -= 1
        while self.board[i2][j2] == player:
            i2 += 1
            j2 += 1
        if i2 - i1 > 5:
            return True
        i1 = i2 = i
        j1 = j2 = j
        while self.board[i1][j2] == player:
            i1 -= 1
            j2 += 1
        while self.board[i2][j1] == player:
            i2 += 1
            j1 -= 1
        if i2 - i1 > 5:
            return True
        return False

    def show(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.board[i, j] == 0:
                    if i == 1:
                        if j == 1:
                            print '┌',
                        elif j == self.size:
                            print '┐',
                        else:
                            print '┬',
                    elif i == self.size:
                        if j == 1:
                            print '└',
                        elif j == self.size:
                            print '┘',
                        else:
                            print '┴',
                    else:
                        if j == 1:
                            print '├',
                        elif j == self.size:
                            print '┤',
                        else:
                            print '┼',
                elif self.board[i, j] == 1:
                    print '●',
                else:
                    print '○',
            print
        print


if __name__ == '__main__':
    gobang = Gobang()
    '''
    gobang.board = numpy.array([
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ])
    print gobang.value(1)
    '''
    player = 1
    gobang.show()
    while True:
        if player == 1:
            i, j = input()
            if gobang.input(i + 1, j + 1, player):
                gobang.show()
                if gobang.win(i + 1, j + 1, player):
                    break
                player = -player
        else:
            i, j = gobang.value(player)
            gobang.input(i + 1, j + 1, player)
            gobang.show()
            if gobang.win(i + 1, j + 1, player):
                break
            player = -player
