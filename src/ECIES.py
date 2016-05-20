import math

def z_is_a_quadratic_non_residue_modulo_p(z, p):
    #FIXME: Still untested
    x_square = z % p
    x = math.sqrt(x_square)
    x_is_a_quadratic_non_residue = isinstance(x, int)
    return x_is_a_quadratic_non_residue

def point_decompress(x):
    #As described on Algorithm 6.4, page 263
    z = (pow(x[0],3) + a*x[0] + b) % p
    if z_is_a_quadratic_non_residue_modulo_p(z, p):
        return "failure"
    else :
        y = int(math.sqrt(z)) % p
        if y % 2 == x[1] % 2:
            return (x[0], y)
        else:
            return (x[0], p - y)

def point_compress(x):
    return (x[0], x[1] % 2)

def encrypt_plaintext(x, k):
    kP = multiply(k, P)
    kQ = multiply(k, Q)
    x0 = kQ[0]
    return (point_compress(kP), (x*x0) % p)

def decrypt_ciphertext(y):
    y1 = y[0]
    y2 = y[1]
    decompressed_point = multiply(m, point_decompress(y1))
    x0 = decompressed_point[0]
    return (y2*modinv(x0, p)) % p


def multiply(k, A):
    #TODO: For Nuno
    #supposedly
    res = A
    for x in range (0, k-1) :
        res = point_add(res, A)

    return res

def egcd(a, b):
    prevx, x = 1, 0;
    prevy, y = 0, 1
    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b
    return a, prevx, prevy


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def point_add(x,y) :
    if(x[0] == y[0]) :
        if(x[1] == y[1]) :
            slope = ((3 * (pow(x[0],2)) + a) % p) * modinv((2*x[1]), p)
            slope = slope % p
        else :
            raise Exception('Point at infinity')
    else :
        slope = ((y[1] - x[1]) % p) * modinv((y[0] - x[0]), p)
        slope = slope % p
    x3 = ((pow(slope,2)) - x[0] - y[0]) % p
    y3 = (slope * (x[0] - x3) - x[1]) % p

    return (x3, y3)






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