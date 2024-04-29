import random

def eea(r0, r1):
    """
    Pre-condition ro > r1 >=0
    :param r0: integer
    :param r1: integer
    :return: (gcd(r0, r1), s, t), where gcd(r0, r1) = s*r0 + t*r1
    """
    s1 = 0
    t0 = 0
    s0 = 1
    t1 = 1
    while r1 > 0:
        q = r0 // r1
        r2 = r0 - q * r1
        s2 = s0 - q * s1
        t2 = t0 - q * t1
        r0 = r1
        r1 = r2
        s0 = s1
        s1 = s2
        t0 = t1
        t1 = t2
    return r0, s0, t0

def dhke(p, alpha, a, b):
    pubA = (alpha ** a) % p
    pubB = (alpha ** b) % p
    shared = (pubB ** pubA) % p
    print(shared)

def inverse(a, m):
    """
    :param a: integer
    :param m: integer or None
    """
    for i in range(0, m):
        if (a * i) % m == 1:
            return i
    return None
    
def get_prime(bits, s):
    """
    :param bits: number of bits in generated primes
    :param s: security parameter
    :return: a probable prime of the length of the specified bits
    """
    while True:
        p = random.randrange(1 << bits - 1, 1 << bits) + 1
        temp = p-1
        u = 0
        while temp%2==0:
            u+=1
            temp = temp//2

        r = temp
        
        if miller_rabin(p, u, r, s):
            return p

def miller_rabin(p, u, r, s):
    for i in range(s):
        a = random.randrange(2, p-2)
        z = mod_pow(a, r, p)
        if (z != 1) and (z != p-1):
            for _ in range(u-1):
                z = mod_pow(z, 2, p)
                if z == 1:
                    return False
            if z != p-1:
                return False
    return True


def mod_pow(x, e, n):
    """
    :param x: base
    :param e: exponent
    :param n: modulus
    :return: x^e mod n
    """
    power_bin = bin(e)[2:]
    result = x
    for bit in power_bin[1:]:
        result = result ** 2 % n
        if bit == '1':
            result = result * x % n
    return result

def key_generation():
    """
    Use the utility functions you wrote to generate RSA keys
    :param bits: the number of bits in n
    :param s: security parameter
    :return: (e,n,d), where (n,e) is a public key and d is a private key
    """
    p = get_prime(10, 5)
    q = get_prime(10, 5)
    n = p * q
    phiN = (p-1)*(q-1)
    # print("p=", p)
    # print("q=", q)
    e = random.randint(1, phiN-1)
    while (eea(e, phiN)[0] != 1):
        e = random.randint(1, phiN-1)
    d = eea(e, phiN)[1] % phiN
    # print("d=", d)
    return (e, n, d)

def encrypt(x, e, n):
    """
    Use the mod_pow funciton to encrypt x
    :param x: plaintext
    :param e: public key
    :param n: publick key
    :return: x^e mod n
    """
    return mod_pow(x, e, n)

def decrypt(y, d, n):
    """
    Use the mod_pow funciton to decrypt y
    :param y: ciphertext
    :param d: private key
    :param n: public key
    :return: y^d mod n
    """
    return mod_pow(y, d, n)