#!/bin/python

from math import sqrt
from math import log

def sieve(upper_bound):
    numbers = [True]*(upper_bound + 1)
    numbers[0] = numbers[1] = False
    primes = []
    for i in range(upper_bound + 1):
        if numbers[i] == True:
            primes.append(i)
            for j in range(i*i, upper_bound+1, i):
                numbers[j] = False
    return primes


def prime_combinations_below(upper_bound):
    primes = sieve(upper_bound // 2) # Only primes < (upper_bound / 2) can be combined with other ones.
    squareable = [x for x in primes if x <= int(sqrt(upper_bound))]
    composable = [x for x in primes if x > int(sqrt(upper_bound))]
    available_numbers = []

    for low_prime in squareable:
        for power in range(1, int(log(upper_bound, low_prime)) + 1):
            available_numbers.append(low_prime**power)
            #print("{}, {}".format(low_prime**power, low_prime**power > upper_bound))
            for big_prime in composable:
                nr = low_prime**power * big_prime
                if nr > upper_bound:
                    break
                available_numbers.append(nr)
    return available_numbers
    

if __name__ == "__main__":
    combinations = prime_combinations_below(200000)
    print(combinations)
    print("Length: {}".format(len(combinations)))