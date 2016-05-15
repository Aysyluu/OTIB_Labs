import numpy as np
from math import tanh, cosh, exp, ceil, factorial
from decimal import *
import itertools as itools



def discretize(x):
    if x >= 0:
        return 1
    else:
        return 0


def bitfield(n):
    bitarray = [int(digit) for digit in bin(n)[2:]]
    while (len(bitarray) < 4):
       bitarray.insert(0,0)
    return bitarray


def count_phi(center, vector):
    bit_vector = bitfield(vector)
    sum = 0
    for i in range(4):
        sum += (bit_vector[i] - center[i]) * (bit_vector[i] - center[i])

    sum = 0 - sum

    return Decimal(exp(sum))


def init_real_out(real_out, net_out):
    for index in range(16):
        real_out[index] = discretize((net_out[index]))



def print_final_weights(_weights):
    print('Final weigths are:')
    for index in range(4):
        print('v({0}): {1}'.format(index, _weights[index]))




def learn(weights, real_out, samples,selection, centers):
    Phi = [0, 0, 0]

    for vector in selection:
        delta = samples[vector] - real_out[vector]

        for index in range(3):
            Phi[index] = count_phi(centers[index], vector)

        weights[0] += learn_rate*delta*1
        for index in range(3):
            weights[index+1] += learn_rate * delta * Phi[index]

    for i in range(16):
        net = weights[0]+count_phi(centers[0], i)*weights[1] + count_phi(centers[1], i)*weights[2] + count_phi(centers[2], i)*weights[3]
        real_out[i] = discretize(net)


def count_hamming_distance(a,b):
    distance = 0
    for index in range(0,16):
        distance += abs(a[index] - b[index])
    return distance


def learn_till_the_end(weights, real_out, net_out, samples, selection, centers, debug):
    init_real_out(real_out, net_out)
    hamming_distance = count_hamming_distance(real_out, samples)
    if (debug == 1):
        print('Epoch {0} with {1} errors \nSamples are: {2}\nReal out is: {3}\n'.format(0, hamming_distance, samples,real_out))
        print(weights)

    for index in range(1, 51):
        learn(weights, real_out, samples, selection, centers)

        hamming_distance = count_hamming_distance(real_out, samples)
        if (debug == 1):
            print('Epoch {0} with {1} errors \nSamples are: {2}\nReal out is: {3}\n'.format(index, hamming_distance, samples,real_out))
            print weights
        if hamming_distance == 0:
            break

    return hamming_distance


def find_min_vector(weights, real_out, net_out, samples, centers):
    size = 15
    hamming_distance = 0
    last_successfull_selection = ()

    while size > 0 and hamming_distance == 0:
        range_list = range(16)

        combination_count = factorial(16)/(factorial(size)*factorial(16-size))
        all_combinations = list(itools.combinations(range_list, size))

        for selection in range(combination_count):
            real_out = [0 for digit in range(16)]
            net_out = real_out
            weights = [Decimal(0) for digit in range(4)]

            current_selection = all_combinations[selection]
            hamming_distance = learn_till_the_end(weights, real_out, net_out, samples, current_selection, centers, 0)
            #print ('Current selection is {0} and Error is {1} and No is {2}'.format(current_selection, hamming_distance, selection))
            if hamming_distance == 0:
                last_successfull_selection = current_selection
                print_final_weights(weights)
                break
        print ('Current size is {0}').format(size-1)
        size -= 1


    print('MINIMAL SELECTION IS {0}'.format(last_successfull_selection))
    weights = [0, 0, 0, 0]
    learn_till_the_end(weights,real_out, net_out, samples_14var, last_successfull_selection, centers, 1)



learn_rate = Decimal(0.3)
delta = Decimal(0)
samples_0var = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
samples_14var = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
real_out = [0 for digit in range(16)]
net_out = real_out
weights = [Decimal(0) for digit in range(4)] #v0, v1, v2, v3

C1 = [0,1,0,0]
C2 = [1,0,0,0]
C3 = [1,1,0,0]
centers = [C1,C2,C3]

getcontext().prec=2


#learn_till_the_end(weights, real_out, net_out, samples_14var, range(16), centers, 1)
find_min_vector(weights, real_out, net_out, samples_14var, centers)


