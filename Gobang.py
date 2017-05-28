#!/usr/bin/env python
# coding:utf-8

import numpy

kinds = {
    1: [
        '.oooo.x',
    ],
    2: [
        'boooo.x',
        'xo.ooox',
        'xoo.oox',
        'x.ooo.x',
        '.o.oo.x',
        '.oo.o.x'
    ],
    3: [
        'booo..x',
        'boo.o.x',
        'bo.oo.x',
        'x.oo..x',
        'x.o.o.x',
    ],
    4: [
        'boo...x',
        'bo.o..x',
        'bo..o.x',
        'bo...ox'
    ],
    5: [
        'xo....x',
        'x.o...x',
        'x..o..x'
    ],
    6: [
        'bo....x',
        'b.o...x',
        'b..o..x',
        'b...o.x',
        'b....ox'
    ]
}


def match_sub(code, mode):
    if len(code) != len(mode):
        return False
    else:
        for i, j in zip(code, mode):
            if j != 'x' and i != j:
                return False
        else:
            return True


def match(code):
    code_r = code[::-1]
    for v, kind in kinds.items():
        for k in kind:
            if match_sub(code, k) or match_sub(code_r, k):
                return 65536 >> v
    else:
        return 0


def encode(value):
    return ''.join(['o' if v == 1 else '.' if v == 0 else 'b' for v in value])


class Gobang:
    def __init__(self, size=15, user_first=True):
        self.size = size
        self.user_first = True
        self.board = numpy.zeros((size, size)).astype(numpy.int32)

    def save(self, filename="status.board"):
        board = self.board.reshape(self.size * self.size) + 1
        board = ''.join(map(lambda x: str(x), board.tolist()))
        with open(filename, 'w') as f:
            f.write(board + "\n")

    def load(self, filename="status.board"):
        with open(filename, 'r') as f:
            board = f.readline()[:-1]
            self.board = numpy.array(map(lambda x: int(x) - 1, list(board))).astype(numpy.int32).reshape([self.size, self.size])

    def value_line(self, dis_1, dis_2, block):
        if dis_2 <= 5:
            return 1 << dis_2
        else:
            if dis_1 > 5:
                return 1024
            else:
                return 256 << (dis_1 if block else (dis_1 + 1))

    def value_one(self, i, j, player=-1):
        v = 0
        board_U = max(i - 4, 0)
        board_D = min(i + 4, self.size - 1)
        board_L = max(j - 4, 0)
        board_R = min(j + 4, self.size - 1)
        # 上-下
        i1 = i2 = i
        while i1 >= board_U and self.board[i1, j] == player:
            i1 -= 1
        while i2 <= board_D and self.board[i2, j] == player:
            i2 += 1
        dis_1 = i2 - i1
        block = True
        while i1 >= board_U and self.board[i1, j] == 0:
            block = False
            i1 -= 1
        while i2 <= board_D and self.board[i2, j] == 0:
            block = False
            i2 += 1
        dis_2 = i2 - i1
        v += self.value_line(dis_1, dis_2, block) - player
        # 左-右
        j1 = j2 = j
        while j1 >= board_L and self.board[i, j1] == player:
            j1 -= 1
        while j2 <= board_R and self.board[i, j2] == player:
            j2 += 1
        dis_1 = j2 - j1
        block = True
        while j1 >= board_L and self.board[i, j1] == 0:
            block = False
            j1 -= 1
        while j2 <= board_R and self.board[i, j2] == 0:
            block = False
            j2 += 1
        dis_2 = j2 - j1
        v += self.value_line(dis_1, dis_2, block) - player
        # 左上-右下
        i1 = i2 = i
        j1 = j2 = j
        while i1 >= board_U and j1 >= board_L and self.board[i1, j1] == player:
            i1 -= 1
            j1 -= 1
        while i2 <= board_D and j2 <= board_R and self.board[i2, j2] == player:
            i2 += 1
            j2 += 1
        dis_1 = i2 - i1
        block = True
        while i1 >= board_U and j1 >= board_L and self.board[i1, j1] == 0:
            block = False
            i1 -= 1
            j1 -= 1
        while i2 <= board_D and j2 <= board_R and self.board[i2, j2] == 0:
            block = False
            i2 += 1
            j2 += 1
        dis_2 = i2 - i1
        v += self.value_line(dis_1, dis_2, block) - player
        # 左下-右上
        i1 = i2 = i
        j1 = j2 = j
        while i2 <= board_D and j1 >= board_L and self.board[i2, j1] == player:
            i2 += 1
            j1 -= 1
        while i1 >= board_U and j2 <= board_R and self.board[i1, j2] == player:
            i1 -= 1
            j2 += 1
        dis_1 = i2 - i1
        block = True
        while i2 <= board_D and j1 >= board_L and self.board[i2, j1] == 0:
            block = False
            i2 += 1
            j1 -= 1
        while i1 >= board_U and j2 <= board_R and self.board[i1, j2] == 0:
            block = False
            i1 -= 1
            j2 += 1
        dis_2 = i2 - i1
        v += self.value_line(dis_1, dis_2, block) - player
        return v

    def value(self, player=-1):
        value_1 = numpy.zeros((self.size, self.size)).astype(numpy.uint32)
        value_2 = numpy.zeros((self.size, self.size)).astype(numpy.uint32)
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == 0:
                    self.board[i, j] = player
                    value_1[i, j] = self.value_one(i, j, player) + 128 - numpy.floor(numpy.sqrt((i - self.size / 2) ** 2 + (j - self.size / 2) ** 2))
                    self.board[i, j] = -player
                    value_2[i, j] = self.value_one(i, j, -player) + 128 - numpy.floor(numpy.sqrt((i - self.size / 2) ** 2 + (j - self.size / 2) ** 2))
                    self.board[i, j] = 0
                else:
                    value_1[i, j] = value_2[i, j] = 0
        max_1 = numpy.max(value_1)
        max_2 = numpy.max(value_2)
        argmax_1 = numpy.where(value_1 == max_1)
        argmax_2 = numpy.where(value_2 == max_2)
        if max_1 >= max_2:
            choice = numpy.random.randint(argmax_1[0].size)
            return argmax_1[0][choice], argmax_1[1][choice]
        else:
            choice = numpy.random.randint(argmax_2[0].size)
            return argmax_2[0][choice], argmax_2[1][choice]

    def input(self, i, j, player=1):
        if 0 <= i < self.size and 0 <= j < self.size:
            if self.board[i, j] == 0:
                self.board[i, j] = player
                return True
            else:
                return False
        else:
            return False

    def show(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == 0:
                    if i == 0:
                        if j == 0:
                            print '┌',
                        elif j == self.size - 1:
                            print '┐',
                        else:
                            print '┬',
                    elif i == self.size - 1:
                        if j == 0:
                            print '└',
                        elif j == self.size - 1:
                            print '┘',
                        else:
                            print '┴',
                    else:
                        if j == 0:
                            print '├',
                        elif j == self.size - 1:
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
    player = 1
    while True:
        gobang.show()
        if player == 1:
            i, j = input()
            if gobang.input(i, j, player):
                gobang.show()
                if gobang.value_one(i, j, player) > 65000:
                    break
                player = -player
        else:
            i, j = gobang.value(player)
            gobang.input(i, j, player)
            gobang.show()
            if gobang.value_one(i, j, player) > 65000:
                break
            player = -player
