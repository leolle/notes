# -*- coding: utf-8 -*-
import numpy as np
import math
import pprint


def cal_e_small(x):
    n = 10
    f = np.arange(1, n+1).cumprod()
    b = np.array([x]*n).cumprod()
    return np.sum(b/f) + 1


def cal_e(x):
    reverse = False
    if x < 0:
        x = -x
        reverse = True
    ln2 = 0.69314718055994529
    c = x / ln2
    a = int(c + 0.5)
    b = x - a * ln2
    y = (2 ** a) * cal_e_small(b)
    if reverse:
        return 1 / y
    return y


t1 = np.linspace(-2, 0, 10, endpoint=False)
t2 = np.linspace(0, 2, 20)
t = np.concatenate((t1, t2))
print(t)
y = np.empty_like(t)
for i, x in enumerate(t):
    y[i] = cal_e(x)
    print('e^', x, ' = ', y[i], ', appx = \t', math.exp(x))
