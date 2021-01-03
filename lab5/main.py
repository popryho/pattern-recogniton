from operator import xor
from math import log
from os import listdir
from numpy import array
from PIL import Image
from datetime import datetime


def recognizer(probabilities_of_bigrams, standard_chars, real_chars, noise):
    """
    The function makes a direct traversal of letters from the last in the text to the first.
    At each step, the set of valid labels is calculated and written to the dictionary as label: value.

    Then the letters are traversed backwards()in the reverse order:
    Starting with a space, we will bypass the letters from the first to the last one and display them on the screen.

    :param probabilities_of_bigrams: probabilities of all bigrams.
    :param standard_chars: numerical interpretation of the alphabet as a dictionary.
    :param real_chars: the numerical representation of the noisy image of the letter from the incoming text.
    :param noise: the Bernoulli distribution parameter
    """
    # straight order
    n = real_chars.shape[1] // 28
    res = {}
    for i in range(n):
        res[i] = {}
        if i == 0:
            for k in standard_chars.keys():
                res[i][k] = func(probabilities_of_bigrams, standard_chars, real_chars, noise, i, k)
        elif 0 < i < n:
            for k in standard_chars.keys():
                res[i][k] = func(probabilities_of_bigrams, standard_chars, real_chars, noise, i, k, res[i - 1])

    # reverse order
    text = list(' ')
    for i in range(n-1, -1, -1):
        char = str()
        if i != 0:
            char = func(probabilities_of_bigrams, standard_chars, real_chars, noise, i, text[-1], res[i - 1], mode=1)
        if i == 0:
            char = func(probabilities_of_bigrams, standard_chars, real_chars, noise, i, text[-1], mode=1)
        print(char, sep='', end='')
        text.append(char)


def func(probabilities_of_bigrams, standard_chars, real_chars, noise, i, prev_char, res_on_prev_step=None, mode=None):
    """
    We have the k_{i}-th markup element by which we maximize the expression.
    k_{i-1}st is the preceding markup element (the prev_char argument).

    The function goes through all possible k_{i} from the alphabet and
    returns the maximum value that is achieved with the best k_{i} for a particular k_{i-1}(prev_char)


    :param probabilities_of_bigrams: Probabilities of all bigrams.
    :param standard_chars: numerical interpretation of the alphabet as a dictionary
    :param real_chars: the numerical representation of the noisy image of the letter from the incoming text.
    :param noise: the Bernoulli distribution parameter

    :param i: the numeric representation of the i-th pictured letter in the noisy text.
    :param prev_char: k_{i-1} markup element. Current element of markup - k_{i}.
    :param res_on_prev_step: a dictionary of possible previous (k_{i-1}) letters with the corresponding values
    obtained in the previous step.

    :param mode: a parameter that indicates in what order the letters are bypassed in the text.
    None if straight order, else - the reverse order

    :return: the maximum value that is achieved with the best k_{i} for a particular k_{i-1}(prev_char)
    """
    res = {}
    for k in standard_chars.keys():
        if res_on_prev_step is None:
            try:
                res[k] = log(get_bigram_prob(probabilities_of_bigrams, prev_char, k)) + \
                         symbol_recognition(standard_chars[k], get_frame(real_chars, i), noise)
            except KeyError:
                pass
        else:
            try:
                res[k] = log(get_bigram_prob(probabilities_of_bigrams, prev_char, k)) + res_on_prev_step[k] + \
                         symbol_recognition(standard_chars[k], get_frame(real_chars, i), noise)
            except KeyError:
                pass
    return max(res.values()) if mode is None else max(res, key=res.get)

