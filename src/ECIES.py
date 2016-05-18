import math

def z_is_a_quadratic_non_residue_modulo_p(z, p):
    #FIXME: Still untested
    x_square = z % p
    x = math.sqrt(x_square)
    x_is_a_quadratic_non_residue = isinstance(x, int)
    return x_is_a_quadratic_non_residue

def point_decompress(x, i):
    #As described on Algorithm 6.4, page 263
    z = (x^3 + a*x + b) % p
    if z_is_a_quadratic_non_residue_modulo_p(z, p):
        return "failure"
    else
        y = math.sqrt(z) % p
        if y == i % 2:
            return (x, y)
        else:
            return (x, P - y)

def point_compress(x, y):
    return (x, y % 2)

def encrypt_plaintext(x, k):
    kP = multiply(k, P)
    kQ = multiply(k, Q)
    x0 = kQ[0]
    return point_compress(kP, (x*x0) % p)

def decrypt_ciphertext(y):
    y1 = y[0]
    y2 = y[1]
    decompressed_point = multiply(m, point_decompress(y1))
    x0 = decompressed_point[0]
    return (y2/x0) % p


def multiply(k, A):
    #TODO: For Nuno
    return (0 ,0)

#Define cryptosystem: K = {(E, P, m, Q, n): Q = mP}
global a, b, p      #E function: f(x) = x^3 + a*x + b (mod p)
global P            #P generated point (is a public key): P = (x_p, y_p)
global m            #m  (is a private key)
global Q            #Q (is a public key): Q = (x_q, y_q)
global n            #n (is a public key)

#E setup
a = 1
b = 6
p = 11

#P setup
P = (2, 7)

#m setup
m = 7

#Q setup
Q = (7, 2)

#n setup
n = 13