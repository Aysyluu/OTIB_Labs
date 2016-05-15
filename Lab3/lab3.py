from __future__ import print_function
from os import listdir
import fnmatch
import numpy as np
from pickle import dump, load

np.set_printoptions(threshold=np.nan)
_LENGTH = 5
_HEIGHT = 5

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def activate_func(figure_vector):
    result = []
    for digit in figure_vector:
        if digit > 0:
            result.append(int(1))
        if digit <= 0:
            result.append(int(-1))
    return result


def read_files(path, names):
    files_list = []
    for file_name in listdir(path):
        if fnmatch.fnmatch(file_name, names):
            files_list.append(file_name)
    return files_list


def print_figure_from_file(opened_file):
    for line in opened_file:
        new_line = ""
        for symbol in line:
            if symbol == '1':
                symbol = bcolors.OKGREEN + symbol + bcolors.ENDC
            if symbol != '\n':
                new_line += symbol
        print(new_line, "")


def print_figure_from_vector(vector):
    for line in np.reshape(vector, (_HEIGHT, _LENGTH)):
        new_line = ""
        for symbol in line:
            if symbol == -1:
                new_line += "0"
            elif symbol == 1:
                new_line += (bcolors.OKGREEN + "1" + bcolors.ENDC)
        print (new_line, "")


def vectorize_figure(opened_file):
    vector = []
    for line in opened_file:
        for symbol in line:
            if symbol == '0':
                vector.append(int('-1'))
                continue
            if symbol != '\n':
                vector.append(int(symbol))
    return vector


#W = np.array(figures_vectors[1]) * W
#W = activate_func(W.tolist()[0])
#print (W)


def learn_patterns(dir_path):
    files = read_files(dir_path, 'pattern_*.txt')
    figures_vectors = []
    _RES = _LENGTH*_HEIGHT
    W = np.mat(np.zeros((_RES, _RES)), dtype=np.int8)

    for name in files:
        print (bcolors.HEADER + dir_path + name + bcolors.ENDC, "")
        f = open(dir_path + name, 'r')
        print_figure_from_file(f)
        f.seek(0)
        current_figure = vectorize_figure(f)
        figures_vectors.append(current_figure)
        file_with_vector = open(dir_path + "vector_" + name, 'w')
        file_with_vector.write(str(current_figure))
        file_with_vector.close()
        f.close()

    for vector in figures_vectors:
        vector = np.array(vector)
        W += np.mat(vector[:, None]) * vector
        np.fill_diagonal(W, 0)
    print (W)

    file_with_weights = open(dir_path + "weights", 'w')
    dump(W, file_with_weights)
    file_with_weights.close()

    return W


def restore_patterns(dir_path):
    files = read_files(dir_path, 'vector_pattern_*.txt')
    weight_matrix_file = open(dir_path + "weights", 'r')
    weight_matrix = load(weight_matrix_file)
    weight_matrix_file.close()
    vectors = []
    for name in files:
        f = open(dir_path + name, 'r')
        for line in f:
            line = line.translate(None, "[]")
            vectors.append(map(int, line.split(',')))
        f.close()

    for i, figure in enumerate(vectors):
        response = np.array(figure) * weight_matrix
        response = activate_func(response.tolist()[0])
        print (bcolors.HEADER + dir_path + files[i] + bcolors.ENDC, "")
        print (figure)
        print_figure_from_vector(response)


#W = learn_patterns("./resources/")
restore_patterns("./resources/")
