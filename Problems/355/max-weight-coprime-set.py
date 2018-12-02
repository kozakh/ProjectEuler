#!/bin/python

"""
    Možnosti:
    - zahrabat se do peřin s knížkou diskrétní matematiky od Habaly
    - genetickej algoritmus
    - simulated annealing
"""

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

"""
    The same as function after, the only difference is that only big_prime*(low_prime**log(upper_bound/big_prime, low_prime)) are added
"""
def squareable_max_prime_combinations(upper_bound):
    primes = sieve(upper_bound)
    composable = [x for x in primes if x*x > upper_bound and x <= (upper_bound//2)]
    squareable = [x for x in primes if x*x <= upper_bound]
    combinations = []
    for i, prime in enumerate(squareable):
        combinations.append([])
        max_power = int(log(upper_bound, prime))
        combinations[i].append((prime**max_power, 0))
        for big_prime in composable:
            if prime * big_prime > upper_bound:
                break
            combinations[i].append((big_prime*(prime**(int(log(upper_bound/big_prime, prime)))), big_prime))
    return combinations

"""
    Numbers of combinations in one bracket: l = [len(x) for x in squareable_max_prime_combinations(200000)]
    Number of all possible combinations: 
        from functools import reduce
        reduce(lambda x, y: x * y, l)

"""


def resolve_conflicts(assignment, combinations, upper_bound):
    conflicts = {x:y for x, y in assignment if len(y) > 1}
    blacklist = {} # Dictionary of low_prime : set(big_primes), where each low_prime is assigned the set of big_primes it can't be used with.
    primes = sieve(upper_bound)
    
    while bool(conflicts):
        for big_prime, low_prime_list in conflicts:
            winner = max(low_prime_list)
            # Make a list of primes to reassign
            conflict_list = low_prime_list.copy()
            conflict_list.remove(winner)
            # We can remove all other assigned low primes, because we're reassigning them in the next loop
            assignment[big_prime] = [winner]
            for low_prime in conflict_list:
                blacklist.setdefault(low_prime, []).append(big_prime)
                for x,y in combinations[primes.index(low_prime)]:
                    if y not in blacklist[low_prime] and x > (primes[i]**int(log(upper_bound, primes[i])) + y):
                        assignment.setdefault(y, []).append(low_prime)
                        break
        conflicts = {x:y for x, y in assignment if len(y) > 1}
    return assignment



"""
    For every low prime finds big prime in such way that

        low_prime * big_prime > low_prime**int(log(upper_bound, low_prime)) + big_prime
"""

def get_max_whose_product_is_bigger_than_sum(combinations, upper_bound):
    result_combinations = []
    primes = sieve(upper_bound)
    big_to_low_primes = {}
    used_big_primes = set()
    for i, c in enumerate(combinations):
        c.sort(key=(lambda x: x[1]), reverse=True)
        max_combinable_big_prime = -1
        max_product = -1
        for x,y in c:
            if x > (primes[i]**int(log(upper_bound, primes[i])) + y): # and y not in used_big_primes:      #Beware (prime**max_power, 0)
                big_to_low_primes.setdefault(y, []).append(primes[i])
                max_combinable_big_prime = y
                max_product = x
                break
        if max_combinable_big_prime != -1:
            result_combinations.append(max_product)
            used_big_primes.add(max_combinable_big_prime)
        else:
            result_combinations.append(primes[i]**int(log(upper_bound, primes[i])))

    return resolve_conflicts(big_to_low_primes, combinations, upper_bound), used_big_primes


"""
    For the integer argument, the function returns a list of lists of tuples in the following structure:
    [ [(squareable_prime**1, 0), (squareable_prime**1 * composable_prime, composable_prime),...], ..., [(max_squareable_prime**max_power * composable_prime)]]
"""
def squareable_prime_combinations(upper_bound):
    primes = sieve(upper_bound)
    composable = [x for x in primes if x*x > upper_bound and x <= (upper_bound//2)]
    squareable = [x for x in primes if x*x <= upper_bound]
    combinations = []
    for i, prime in enumerate(squareable):
        combinations.append([])
        max_power = int(log(upper_bound, prime))
        for power in range(1, max_power + 1):
            combinations[i].append((prime**power, 0))
            for big_prime in composable:
                if prime**power * big_prime > upper_bound:
                    break
                combinations[i].append((prime**power * big_prime, big_prime))
    return combinations


def reduce_combinations(combinations):
    for l in combinations:
        l.sort(key=lambda tup: tup[0], reverse=True)
    return [l[:3] for l in combinations]


"""
    No backtracking.
    Even when considering 2 possibilities for each of the 86 squareable primes, the time,
    ((2**86)//3 000 000 000)/(60*60*24*365.3) = 817 137 154.0486793 years,
    is unbearable.
"""


#def maximize_combinations_bt(upper_bound):
    #combinations = reduce_combinations(squareable_prime_combinations(upper_bound))
    #max = 0
    #for 


def maximize(prime, prime_list, upper_bound, conflicts,blacklist):
    max_power = int(log(upper_bound, prime))
    max = prime**max_power
    used_prime = -1
    power = -1
    for i in range(max_power+1): # TODO range(max_power + 1)!!! But that doesn't change anything, since max is originally set to max power.
        for p in prime_list:
            candidate = prime**i * p
            if candidate > upper_bound or p in blacklist:
                continue
            if candidate > max:
                max = candidate
                used_prime = p
                power = i
    if used_prime != -1:
        prime_list.remove(used_prime)
    #    print("Used {}".format(used_prime))
    #if used_prime != -1:
    #    conflicts.setdefault(used_prime, []).append((prime, power))
    return max

"""
    No, bad approach.
    Should I add 10 or 5 and 8?

"""

def Co(n):
    primes = sieve(n)
    copiable = [x for x in primes if x > (n//2)]
    composable = [x for x in primes if x*x > n and x <= (n//2)]
    squareable = [x for x in primes if x*x <= n]
    result_list = copiable.copy()
    conflicts = dict()
    for p in reversed(squareable):              #Loop through the primes in reversed order. TODO revise, not necessarily a better way.
    #for p in squareable:
        result_list.append(maximize(p,composable,n,conflicts, []))
    for p in composable:
        result_list.append(p) # Add all unused primes from list
    result_list.append(1)
    print(conflicts)
    for key,val in conflicts.items():
        if len(val) > 1:
            print("{}: {}".format(key,val))
    #print(result_list)
    #print(copiable)
    #print(len(copiable))
    #print(composable)
    #print(len(composable))
    #print(squareable)
    #print(len(squareable))
    return sum(result_list)

if __name__ == "__main__":
    print("Sum: {}".format(Co(30)))