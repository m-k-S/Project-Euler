# @m-k-S [11/2/15]
# Project Euler 516
# 5-Smooth Totients
# Find the sum of the numbers n not exceeding 10^12 such that Euler's totient function phi(n) is a 5-smooth number, modulo 2^32

from math import floor, log
import time
from random import randrange

# Miller-Rabin primality test
def is_prime(n):
    numtrials = 5
    assert n >= 2
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)

    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True

    for i in range(numtrials):
        a = randrange(2, n)
        if try_composite(a):
            return False

    return True

# Combines elements in a list such that they are less than an arbitrary limit
def limited_combine(nums, limit):
    products = set((1,))

    for factor in nums:
        new_products = set()
        for prod in products:
            x = factor * prod
            if x < limit+1:
                new_products.add(x)
        products.update(new_products)

    return list(products)

startTime = time.time()
N = 10**12
Modulus = 2**32
Primes = [2, 3, 5]

# Creating a list of all powers of 2, 3, and 5 below N
primePowers = []
for prime in Primes:
    for i in range(1,int(floor(log(N, prime)))+1):
        primePowers.append(prime**i)

# Creating a list of all Hamming numbers below N
Hammings = limited_combine(primePowers, N)

# Creating a list of all primes that are one more than a Hamming number
smoothPrimesD = []
for i in Hammings:
    if is_prime(i+1):
        smoothPrimesD.append(i+1)
# Removing 2, 3, and 5
smoothPrimesD = smoothPrimesD[3:]

# The numbers whose totients are 5-smooth are combinations of the above primes and Hamming numbers
# phi(p^i q^j r^k...) = p^(i-1) q^(j-1) r^(k-1) (p-1) (q-1) (r-1)...
Totients = smoothPrimesD + primePowers
SmoothTotients = limited_combine(Totients, N)
print sum(SmoothTotients) % Modulus

endTime = time.time()
print "Total elapsed time: " + str(endTime - startTime) + " seconds."
