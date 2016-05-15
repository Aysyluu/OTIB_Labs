import numpy as np
from math import tanh, cosh, exp, ceil, factorial
from decimal import *
import itertools as itools


def discretize(x):
    if x >= Decimal(0.5):
        return 1
    else:
        return 0


def activate_func1(x):
    if x >= 0:
        return 1
    else:
        return 0


def activate_func_derivate1(x):
    return 1


def activate_func3(x):
    return Decimal(1/(1+exp(-x)))


def activate_fun2(x):
    return Decimal(0.5*(x/(1+abs(x) + 1)))


def activate_func_derivate2(x):
    return Decimal(pow(1 - abs(x / (1 + abs(x))), 2) * 0.5)


def activate_func_derivate3(x):
    return activate_func3(x) * (1 - activate_func3(x))


def bitfield(n):
    bitarray = [int(digit) for digit in bin(n)[2:]]
    while (len(bitarray) < 4):
       bitarray.insert(0,0)
    return bitarray


def init_real_out(real_out, net_out):
    for index in range(16):
        real_out[index] = discretize(activate_function(net_out[index]))


def print_final_weights(_weights):
    print('Final weigths are:')
    for index in range(5):
        print('w({0}): {1}'.format(index, _weights[index]))


def learn(weights, real_out, samples,selection):
    for index in selection:
        delta = samples[index] - real_out[index]
        weighted_sum = 0

        current_vector = bitfield(index)
        net = weights[0] + weights[1]*current_vector[0] + weights[2]*current_vector[1] + weights[3]*current_vector[2] + weights[4]*current_vector[3]

        weights[0] += learn_rate*delta*1
        for inner_index in range(4):
            weights[inner_index+1] += learn_rate * delta * activate_function_derivative(net) * current_vector[inner_index]
            weighted_sum += (weights[inner_index+1] * current_vector[inner_index])

    for index in range(16):
        current_vector = bitfield(index)
        net = weights[0] + weights[1]*current_vector[0] + weights[2]*current_vector[1] + weights[3]*current_vector[2] + weights[4]*current_vector[3]
        real_out[index] = discretize(activate_function(net))


def count_hamming_distance(a,b):
    distance = 0
    for index in range(0,16):
        distance += abs(a[index] - b[index])
    return distance


def learn_till_the_end(weights, real_out, net_out, samples, selection, debug):
    init_real_out(real_out, net_out)
    hamming_distance = 0
    hamming_distance = count_hamming_distance(real_out, samples)
    if (debug == 1):
        print('Epoch {0} with {1} errors \nReal out is: {2}'.format(0, hamming_distance, real_out))
        print('W[0] = {} W[1] = {} W[2] = {} W[3] = {} W[4] = {}\n'.format(weights[0].normalize(),
                                                                           weights[1].normalize(),
                                                                           weights[2].normalize(),
                                                                           weights[3].normalize(),
                                                                           weights[4].normalize()))

    for index in range(1, 31):
        learn(weights, real_out, samples, selection)

        hamming_distance = count_hamming_distance(real_out, samples)
        if (debug == 1):
            print('Epoch {0} with {1} errors \nReal out is: {2}'.format(index, hamming_distance, real_out))
            print('W[0] = {} W[1] = {} W[2] = {} W[3] = {} W[4] = {}\n'.format(weights[0].normalize(),
                                                                               weights[1].normalize(),
                                                                               weights[2].normalize(),
                                                                               weights[3].normalize(),
                                                                               weights[4].normalize()))
        if hamming_distance == 0:
            break

    return hamming_distance


def find_min_vector(_weights, _real_out, _net_out, _samples):
    size = 15
    hamming_distance = 0
    current_selection = 0
    last_successfull_selection = ()
    while size > 0 and hamming_distance == 0:
        hamming_distance = 0
        range_list = range(16)
        combination_count = factorial(16)/(factorial(size)*factorial(16-size))
        all_combinations = list(itools.combinations(range_list, size))
        for selection in range(combination_count):
            current_selection = all_combinations[selection]

            _real_out = [0 for digit in range(16)]
            _net_out = _real_out
            _weights = [Decimal(0) for digit in range(5)]

            hamming_distance = learn_till_the_end(_weights, _real_out, _net_out, _samples, current_selection, 0)
            print ('Current selection is {0} and Error is {1} and No is {2}'.format(current_selection, hamming_distance, selection))
            if hamming_distance == 0:
                last_successfull_selection = current_selection
                print_final_weights(_weights)
                break
        print ('Current size is {0}').format(size-1)
        size -= 1


    print('MINIMAL SELECTION IS {0}'.format(last_successfull_selection))



learn_rate = Decimal(0.3)
delta = Decimal(0)
samples_example = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
samples_14var = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
real_out = [0 for digit in range(16)]
net_out = real_out
weights = [Decimal(0) for digit in range(5)] #x0, x1, x2...


getcontext().prec=2
activate_function = activate_func1
activate_function_derivative = activate_func_derivate1


#learn_till_the_end(weights, real_out, net_out, samples_14var, range(16), 1)
find_min_vector(weights, real_out, net_out, samples_14var)



