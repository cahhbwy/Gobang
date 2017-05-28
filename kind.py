#!/usr/bin/env python
# coding:utf-8

import itertools

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


for v in itertools.product([-1, 0, 1], repeat=7):
    if v.count(-1) > 2:
        continue
    c = encode(v)
    if match(c) == 0:
        print c
