#!/bin/python

"""
    Ugly mess. My uninformed idea of sieve of Eratosthenes.
"""
def eratosthenes_sieve(upper_bound):
    numbers = [x for x in range(upper_bound)]
    numbers = [True] * upper_bound
    primes = [] #Or set, doesn't matter, I want it ordered
    composites = set()
    composites.add(1)
    index = 2
    while index < upper_bound:
        if numbers[index] > 0:
            current_prime = numbers[index]
            primes.append(current_prime)
            current_prime_power = current_prime
            current_prime_powers = set()
            #Add all
            while current_prime_power < upper_bound:
                current_prime_powers.add(current_prime_power)
                current_prime_power *= current_prime
            #Contains just the composite numbers that include number[index] in its factorization
            composites_of_current_power = {x*y for x in current_prime_powers for y in composites if x*y < upper_bound}
            for x in composites_of_current_power:
                numbers[x] = 0 # I'm deleting the primes too by this
            composites.update(composites_of_current_power)
        index += 1
    return primes


"""
    This is actually pretty. But i use a different sieve implementation.
"""

def primes_sieve2(limit):
    a = [True] * limit                          # Initialize the primality list
    a[0] = a[1] = False
    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in range(i*i, limit, i):     # Mark factors non-prime
                a[n] = False

"""
    Without conflict resolution.
"""

def get_max_whose_product_is_bigger_than_sum(combinations, upper_bound):
    result_combinations = []
    primes = sieve(upper_bound)
    used_big_primes = set()
    for i, c in enumerate(combinations):
        c.sort(key=(lambda x: x[1]), reverse=True)
        max_combinable_big_prime = -1
        max_product = -1
        for x,y in c:
            if x > (primes[i]**int(log(upper_bound, primes[i])) + y) and y not in used_big_primes:      #Beware (prime**max_power, 0)
                max_combinable_big_prime = y
                max_product = x
                break
        if max_combinable_big_prime != -1:
            result_combinations.append(max_product)
            used_big_primes.add(max_combinable_big_prime)
        else:
            result_combinations.append(primes[i]**int(log(upper_bound, primes[i])))
    return used_big_primes, result_combinations