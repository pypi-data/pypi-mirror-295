import random
from sympy import mod_inverse, isprime, nextprime
import math

def generate_prime(bits=512):
    while True:
        p = nextprime(random.getrandbits(bits))
        if isprime(p):
            return p

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


class PHE:

    @staticmethod
    def keygen(bits=64):
        p = generate_prime(bits)
        q = generate_prime(bits)
        n = p * q
        lambda_n = lcm(p - 1, q - 1)
        g = n + 1
        mu = mod_inverse((pow(g, lambda_n, n * n) - 1) // n, n)
        public_key = (n, g)
        private_key = (lambda_n, mu)
        return public_key, private_key

    @staticmethod
    def encrypt(public_key, plaintext, r=None):
        n, g = public_key
        if r is None:
            r = random.randint(1, n-1)
        n2 = n * n
        c = (pow(g, plaintext, n2) * pow(r, n, n2)) % n2
        return c

    @staticmethod
    def decrypt(public_key, private_key, ciphertext):
        n, g = public_key
        lambda_n, mu = private_key
        n2 = n * n
        x = pow(ciphertext, lambda_n, n2)
        Lx = (x - 1) // n
        plaintext = (Lx * mu) % n
        return plaintext

    @staticmethod
    def homomorphic_add(c1, c2, public_key):
        n, _ = public_key
        n2 = n * n
        return (c1 * c2) % n2