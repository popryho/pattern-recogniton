from PIL import Image
from os import listdir
from pandas import read_json, concat
from numpy import array


def get_probabilities_of_bigrams(path_to_frequencies) -> dict:
    """
    Function that converts frequencies of bigram into their probabilities.
    :param path_to_frequencies: The path to json file containing frequencies.
    :return: Object with probabilities. type: dict.
    """
    df = read_json(path_to_frequencies, typ='series').to_frame('frequencies').reset_index()
    df.rename(columns={'index': 'labels'}, inplace=True)

    df1 = df.labels.apply(lambda x: x[0])
    df.rename(columns={'labels': 'labels1'}, inplace=True)
    df = concat([df, df1], axis=1)
    agg = df.groupby(['labels']).sum()
    df = df.join(agg, on='labels', lsuffix='_caller', rsuffix='_other')

    df.frequencies_caller = df.frequencies_caller / df.frequencies_other
    df = df.set_index('labels1')
    df.drop(['frequencies_other', 'labels'], axis=1, inplace=True)
    return df.to_dict()['frequencies_caller']


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


def get_frame(input_image, s):
    """
    You can see the noisy text on the incoming image.
    Each letter of the text is shown on a 28 x 28 frame.
    This function returns the numeric representation of the s-th pictured letter

    :param input_image: numeric representation of an image
    :param s: number of a frame
    :return: the numeric representation of the s-th pictured letter in the noisy text
    """
    n, m = input_image.shape
    a = m // n  # number of letters in the text
    assert 0 <= s < a
    return input_image[:, (a-s-1)*28:(a-s)*28]
