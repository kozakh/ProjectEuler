#!/bin/python

from math import sqrt

def factorize(n):
    factors = []
    stop = int(sqrt(n))
    current_factor = 2
    factor_multiplicity = 0
    while current_factor <= stop:
        while (n % current_factor) == 0:
            factor_multiplicity += 1
            n //= current_factor
        if factor_multiplicity > 0:
            factors.append((current_factor, factor_multiplicity))
            factor_multiplicity = 0
        current_factor += 1
    if n != 1:
        factors.append((n,1))
    return factors

def product(lst):
    prod = 1
    for x in lst:
        prod *= x
    return prod

def get_divisors(factorization):
    return product([(y + 1) for (x,y) in factorization])

def main():
    MAX = 10**7
    prev_divisors = get_divisors(factorize(2))
    total = 0
    n = 3

    while n < MAX:
        current_divisors = get_divisors(factorize(n))
        if prev_divisors == current_divisors:
            total += 1
        prev_divisors = current_divisors
        n += 1
        if (n % 10**5) == 0:
            print("At {}".format(n))

    print("Number of neighboring numbers with the same number of divisors: {}".format(total))

if __name__ == "__main__":
    main()
