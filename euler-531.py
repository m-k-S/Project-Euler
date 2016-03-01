# @m-k-S [1/12/16]
# Project Euler 531
# Chinese Leftovers
# Find sum(f(n,m)) for 1000000 < n < m < 1005000, where f(n,m) = g(phi(n),n,phi(m),m) and g(a,n,b,m) is a solution x to the system x = a mod n, x = b mod m

import time
from itertools import combinations
from fractions import gcd

# Checks two numbers to see if one is a power of the other
def is_power(a, b):
    if a > b:
        a, b = b, a
    while a != b:
        if b % a != 0:
            return False
        b //= a
    if b == a:
        return True

# Implementation of the extended Euclidean algorithm
def e_gcd(a, b):
    x, y, lx, ly = 0, 1, 1, 0
    while b:
        a, (q, b) = b, divmod(a, b)
        x, lx = lx - q*x, x
        y, ly = ly - q*y, y

    return lx, ly, a

# Factorizes a number into its prime powers
def factorize(n):
    primfac = []
    d = 2
    i = -1
    while d <= n:
        if n % d == 0:
            primfac.append(1)
            i += 1
        while (n % d) == 0:
            primfac[i] *= d
            n //= d
        d += 1

    return primfac

# Solution to a system of two linear congruences - will break down each modulus into its factors to create a coprime system
def crt(a, n, b, m):
    ans = 0
    nfactors = primeFactorizations[n]
    mfactors = primeFactorizations[m]
    n = n + 1000000
    m = m + 1000000

    if a == b and (n % 2) != (m % 2): return 0
    for nfactor in nfactors:
        for mfactor in mfactors:
            if nfactor == mfactor and a != b:
                return 0
            else:
                if nfactor > mfactor:
                    mfactors.remove(mfactor)
                    m //= mfactor
                if mfactor > nfactor:
                    nfactors.remove(nfactor)
                    n //= nfactor
                if mfactor == nfactor:
                    mfactors.remove(mfactor)
                    m // mfactor

    check = gcd(n, m)
    if (a % check) != (b % check): return 0

    checklista = []
    checklistb = []

    for factor in nfactors:
        newa = a % factor
        modulus = (n*m) // factor
        checklista.append((newa, factor))
        r, s, d = e_gcd(factor, modulus)
        ans += newa*s*modulus

    for factor in mfactors:
        newb = b % factor
        modulus = (n*m) // factor
        checklistb.append((newb, factor))
        r, s, d = e_gcd(factor, modulus)
        ans += newb*s*modulus

    for na, moda in checklista:
        for nb, modb in checklistb:
            if (na % check) != (nb % check): return 0

    return ans % (n*m)

# Euler's totient function
def totient(n):
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 1
    if n > 1:
        result -= result // n
    return result

startTime = time.time()

# Populating lists of totients and prime factorizations to avoid recalculating during system solving
Totients = []
primeFactorizations = []
for i in range(1000000, 1005000):
    Totients.append(totient(i))
    primeFactorizations.append(factorize(i))

# Iterating through the intervals
Answer = 0
for n in range(0, 4999):
    for m in range(n+1, 5000):
        Answer += crt(Totients[n], n, Totients[m], m)

print Answer

endTime = time.time()
print "Total elapsed time: " + str(endTime - startTime) + " seconds."
