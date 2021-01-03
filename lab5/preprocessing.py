from PIL import Image
from os import listdir
from re import search
from json import load
from pandas import DataFrame
from numpy import array


def get_probabilities_of_bigrams(path_to_frequencies) -> dict:
    """
    Function that converts frequencies of bigram into their probabilities.
    :param path_to_frequencies: The path to json file containing frequencies.
    :return: Object with probabilities. type: dict.
    """
    with open(path_to_frequencies) as json_file:
        frequencies = load(json_file)

    df = DataFrame(frequencies, index=[0])
    return (df / df.sum(axis=1)[0]).to_dict(orient='records')[0]


def get_bigram_prob(probabilities_of_bigrams, a, b) -> float:
    """
    Conditional probabilities of bigram:
    In the first place of conditional probability there is that symbol
    which in the text is the following. p(b|a)
    :param probabilities_of_bigrams: probabilities of all bigrams
    :param a: previous character
    :param b: next character
    :return: the probability of the required bigram, type: float
    """
    return probabilities_of_bigrams[a + b]


def get_char(file_name) -> str:
    """
    The function is needed to extract the name of the letter
    from the name of the file in which it is located.
    :param file_name: the name of the file that contains the letter.
    :return: letter name, type: str
    """
    if len(file_name) == 5:
        return file_name[0]
    else:
        return r' '


def get_alphabet(path_to_alphabet) -> dict:
    """
    :param path_to_alphabet: path to directory containing letter images
    :return: numerical interpretation of the alphabet as a dictionary
    """
    abc = {}
    alphabet_files = listdir(path=path_to_alphabet)
    for filename in alphabet_files:
        input_image = array(Image.open(path_to_alphabet + filename)).astype(dtype='int64')
        abc[get_char(filename)] = input_image
    return abc


def get_noise(file_name) -> float:
    """
    Get noise from file_name using regular expression
    :param file_name: file name that contains noise in the end of the name
    :return: noise (float)
    """
    match = search(r'[01]\.\d*', file_name[-9:-3])
    return float(match[0]) if match else 0.
