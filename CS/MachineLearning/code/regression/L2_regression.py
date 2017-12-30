# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def regression(data, alpha, lamda):
    n = len(data[0]) - 1
    theta = np.zeros(n)
    for times in range(100):
        for d in data:
            x = d[:-1]
            y = d[-1]
            g = np.dot(theta, x) - y
            theta = theta - alpha * g * x + lamda * theta
        print times, theta
    return theta


