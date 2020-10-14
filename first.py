import asyncio
import doctest
import json
from math import log

import numpy as np
import websockets
from operator import xor


def digit_recognition(standards, digit, noise) -> str:
    """
    Function to find the nearest digit
    :param standards: dictionary with digit names as keys and corresponding matrices as values in the form
    :param digit: binary matrix representing the problem
    :param noise: noise
    :return: string with the nearest digit to input

    >>> digit_recognition(standards={\
    "0":[[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],\
    "1":[[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],\
    "2":[[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],\
    "3":[[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]],\
    "4":[[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],\
    "5":[[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],\
    "6":[[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],\
    "7":[[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,0,0]],\
    "8":[[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],\
    "9":[[1,1,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]]},\
     digit=[[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],\
     noise=0.4)
    '1'
    """

    mses = {}

    for k in range(len(standards)):
        res = 0

        standards[str(k)] = np.array(standards[str(k)])
        digit = np.array(digit)

        for i in range(len(digit)):
            for j in range(len(digit[0])):
                res += xor(digit[i][j], standards[str(k)][i][j]) * log(noise) + \
                        xor(xor(1, digit[i][j]), standards[str(k)][i][j]) * log(1 - noise)

        mses[str(k)] = res
    print(mses)

    return max(mses, key=mses.get)
