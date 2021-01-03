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


def symbol_recognition(standard_char, real_char, noise) -> float:
    """
    A function that calculates the unary constraints of a problem.
    :param standard_char: a numeric representation of an image containing the canonical letter of the alphabet
    :param real_char: the numerical representation of the noisy image of the letter from the incoming text.
    :param noise: the Bernoulli distribution parameter
    :return: q - the unary constraints of a problem | q(k)
    """
    q = 0
    for i in range(len(real_char)):
        for j in range(len(real_char[0])):
            if noise != 1 and noise != 0:
                q += xor(real_char[i][j], standard_char[i][j]) * log(noise) + \
                     xor(xor(1, real_char[i][j]), standard_char[i][j]) * log(1 - noise)
            elif noise == 1:
                q += xor(real_char[i][j], standard_char[i][j])
            elif noise == 0:
                q += xor(xor(1, real_char[i][j]), standard_char[i][j])
    return q


def get_input_image_with_noise(path_to_input_folder, n):
    """
    Function for rendering incoming image.
    :param path_to_input_folder: path to the folder containing the input files, namely images with text
    :param n: file number in the input directory
    :return: numerical representation of an image with text and the Bernoulli distribution parameter(noise)
    """
    input_phrases = listdir(path=path_to_input_folder)

    filename = input_phrases[n]
    im = Image.open(path_to_input_folder + filename)
    input_image = array(im).astype(dtype='int64')
    noise = get_noise(filename)

    print('noise: ', noise, 'filename:', '\n'+filename)
    im.show()
    return input_image, noise


if __name__ == '__main__':

    from preprocessing import (
        get_probabilities_of_bigrams,
        get_bigram_prob,
        get_alphabet,
        get_frame,
        get_noise,
    )

    frequencies_path = 'data/frequencies.json'
    alphabet_path = 'data/alphabet/'
    input_path = 'data/input/'

    index = 19  # file number in the 'input' directory

    bigrams = get_probabilities_of_bigrams(frequencies_path)
    alphabet = get_alphabet(alphabet_path)
    x, p = get_input_image_with_noise(input_path, index)

    #  try to figure out what is shown on the image while the program compute it

    start_time = datetime.now()
    recognizer(bigrams, alphabet, x, p)
    end_time = datetime.now()

    print('\nDuration: {}'.format(end_time - start_time))
