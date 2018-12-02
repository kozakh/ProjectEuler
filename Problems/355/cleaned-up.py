#/bin/python

from math import log
import sys

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


def resolve_conflicts(assignment, combinations, upper_bound):
    conflicts = {x:y for x, y in assignment.items() if len(y) > 1}
    blacklist = {} # Dictionary of low_prime : set(big_primes), where each low_prime is assigned the set of big_primes it can't be used with.
    primes = sieve(upper_bound)
    
    while bool(conflicts):
        for big_prime, low_prime_list in conflicts.items():
            winner = max(low_prime_list)
            # Make a list of primes to reassign
            conflict_list = low_prime_list.copy()
            conflict_list.remove(winner)
            # We can remove all other assigned low primes, because we're reassigning them in the next loop
            assignment[big_prime] = [winner]
            for low_prime in conflict_list:
                blacklist.setdefault(low_prime, []).append(big_prime)
                combinations[primes.index(low_prime)].sort(key=(lambda x: x[1]), reverse=True)
                for x,y in combinations[primes.index(low_prime)]:
                    if y not in blacklist[low_prime] and x > (low_prime**int(log(upper_bound, low_prime)) + y):
                        assignment.setdefault(y, []).append(low_prime)
                        break
                    elif y == 0:
                        assignment.setdefault(0, []).append(low_prime)  # The single powers are added to 0's list. Mind that in calling function.
                        break
                    # TODO elif just the power of low prime is found. Maybe add it to 0:[]
        conflicts = {x:y for x, y in assignment.items() if len(y) > 1}
    return assignment

def resolve_conflicts_in_brackets(assignment, low_p_to_big_p):
    conflicts = {x:y for x, y in assignment.items() if x != 0 and len(y) > 1}   # Exclude 0 from conflicts. 0 means the low_prime**max_power isn't combined with anything.
    low_p_index_to_sums = {} # Stores the index of low_prime to its array of (big_prime, sum).
    # Resolve all conflicts by finding the low_prime, whose shift will least decrease the total sum in its bracket.
    while bool(conflicts):
        for big_p, low_p_list in conflicts.items():
            # Initialize the index - represents number of reassignments
            for p in low_p_list:
                if p not in low_p_index_to_sums:
                    low_p_index_to_sums[p] = 0
            differences = {p:low_p_to_big_p[p][low_p_index_to_sums[p]][1] - low_p_to_big_p[p][low_p_index_to_sums[p] + 1][1] for p in low_p_list}
            winner = max(differences.keys(), key=(lambda key: differences[key])) # Get the prime with maximum difference between current and next lower sum in its bracket.
            to_reassign = low_p_list.copy()
            to_reassign.remove(winner)
            assignment[big_p] = [winner]
            for low_p in to_reassign:
                low_p_index_to_sums[low_p] += 1 # Increment the number of reassignments
                #            low_p:[(big_p, sum)]
                next_big_p = low_p_to_big_p[low_p][low_p_index_to_sums[low_p]][0]
                assignment.setdefault(next_big_p, []).append(low_p)
        conflicts = {x:y for x, y in assignment.items() if x != 0 and len(y) > 1}
    return assignment

def maximize_low_prime_brackets(upper_bound):
    primes = sieve(upper_bound)
    squareable = [x for x in primes if x*x <= upper_bound]
    composable = [x for x in primes if x*x > upper_bound and x <= (upper_bound//2)]
    composable_sum = sum(composable)
    # Resulting structures
    low_p_to_big_p = {} # low_p: [(big_p, sum)]
    assignment = {} # big_p: [low_p]
    # Find all combinations of big_primes and low_primes and their sums with unused big_primes
    for low_p in squareable:
        low_p_to_big_p.setdefault(low_p, [])
        for big_p in composable:
            sum_in_bracket = big_p * low_p**int(log(upper_bound/big_p, low_p)) + composable_sum - big_p
            low_p_to_big_p[low_p].append((big_p, sum_in_bracket))
        # Add the maximum power of low_prime without being composed
        low_p_to_big_p[low_p].append((0, low_p**int(log(upper_bound, low_p)) + composable_sum))
        sorted_bracket = low_p_to_big_p[low_p].sort(key=(lambda x: x[1]), reverse=True) # Sort by total sum
        #                                    low_p:[(big_p, sum)]
        assignment.setdefault(low_p_to_big_p[low_p][0][0], []).append(low_p)
    final_assignment = resolve_conflicts_in_brackets(assignment, low_p_to_big_p)
    result_sq_and_comp = []
    # Add squared only low_primes
    if 0 in final_assignment:
        for low_p in final_assignment[0]:
            result_sq_and_comp.append(low_p**int(log(upper_bound, low_p)))
    del final_assignment[0]
    # Add compositions of squared low_prime * big_prime
    for big_p, low_p_list in final_assignment.items():
        if len(low_p_list) > 1:
            print("ERROR in conflict resolution: {} {}".format(big_p, low_p_list))
            sys.exit()
        if len(low_p_list) == 0:
            continue
        result_sq_and_comp.append(low_p_list[0]**int(log(upper_bound/big_p, low_p_list[0])) * big_p)
    # Add remaining big_primes
    for big_p in composable:
        if big_p not in final_assignment.keys():
            result_sq_and_comp.append(big_p)
    return result_sq_and_comp

def Co2(n):
    primes = sieve(n)
    copiable = [x for x in primes if x > (n//2)]
    result_list = [1]
    result_list.extend(copiable)
    result_list.extend(maximize_low_prime_brackets(n))
    return sum(result_list)


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
            if x > (primes[i]**int(log(upper_bound, primes[i])) + y): # and y not in used_big_primes:      #Beware (prime**max_power, 0)            # This might be the mistake in assumption. We want to maximize at least the low_prime**max_power * big_prime + sum(other_big_primes)
                big_to_low_primes.setdefault(y, []).append(primes[i])
                max_combinable_big_prime = y
                max_product = x
                break
            elif y == 0:     # Max power of the low prime is bigger than any combination
                result_combinations.append(primes[i]**int(log(upper_bound, primes[i])))
                break
        #else:      # Replaced by resolve_conflicts
        #    result_combinations.append(max_product)
        #    used_big_primes.add(max_combinable_big_prime)
    big_to_low_assignment = resolve_conflicts(big_to_low_primes, combinations, upper_bound)
    if 0 in big_to_low_assignment:
        for low_prime in big_to_low_assignment[0]:
            result_combinations.append(low_prime**int(log(upper_bound, low_prime)))
        del big_to_low_assignment[0]

    for big_p, low_p_list in big_to_low_assignment.items():
        if len(low_p_list) > 1:
            print("ERROR in conflict resolution: {} {}".format(big_p, low_p_list))
            sys.exit()
        if len(low_p_list) == 0:
            continue
        result_combinations.append(low_p_list[0]**int(log(upper_bound/big_p, low_p_list[0])) * big_p)
        used_big_primes.add(big_p)
            
    return result_combinations, used_big_primes


def Co(n):
    primes = sieve(n)
    copiable = [x for x in primes if x > (n//2)]
    composable = [x for x in primes if x*x > n and x <= (n//2)]
    squareable = [x for x in primes if x*x <= n]
    print(squareable)
    result_list = [1]   # Adding one
    result_list.extend(copiable)    # Adding the primes too big to form a composed number
    result_combined, used_composable = get_max_whose_product_is_bigger_than_sum(squareable_max_prime_combinations(n), n)
    result_list.extend(result_combined)    # Adding all possible combined numbers
    print(composable)
    print(used_composable)
    print(result_list)
    for prime in composable:
        if prime not in used_composable:
            result_list.append(prime)      # Adding all unused composable prime numbers
            
    print(result_list)
    return sum(result_list)


if __name__ == "__main__":
    print("Sum: {}".format(Co2(200000)))
