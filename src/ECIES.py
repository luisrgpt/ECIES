


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def tonelli(n, p):

    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r


def point_decompress(x):

    # As described on Algorithm 6.4, page 263
    z = (pow(x[0], 3) + a*x[0] + b) % p

    y = tonelli(z, p)
    if y % 2 == x[1] % 2:
        return x[0], y
    else:
        return x[0], p - y


def point_compress(x):

    return x[0], x[1] % 2


def encrypt_plaintext(x, k) :

    kP = multiply(k, P)
    kQ = multiply(k, Q)
    x0 = kQ[0]
    return point_compress(kP), (x*x0) % p


def decrypt_ciphertext(y):
    y1 = y[0]
    y2 = y[1]
    decompressed_point = multiply(m, point_decompress(y1))
    x0 = decompressed_point[0]
    return (y2 * invmod(x0, p)) % p


def multiply(k, A):

    N1 = A
    N2 = 'Origin'
    stringK = bin(k);
    klen = len(stringK);

    for i  in range(klen-1, 1, -1) :
        if stringK[i] == '1' :
            N2 = point_add(N2, N1);

        N1 = point_add(N1, N1)
    return N2


def invmod(x, mod):

    if x % mod == 0:
        raise Exception('modular inverse does not exist')
    return pow(x, mod-2, mod)


def point_add(x,y) :

    if x == 'Origin':
        return y;
    elif y == 'Origin':
        return x;
    if x[0] == y[0]:
        if x[1] == y[1] :
            slope = ((3 * (pow(x[0], 2)) + a) % p) * invmod((2*x[1]), p)
            slope = slope % p
        else:
            return 'Origin'
    else:
        slope = ((y[1] - x[1]) % p) * invmod((y[0] - x[0]), p)
        slope = slope % p
    x3 = ((pow(slope, 2)) - x[0] - y[0]) % p
    y3 = (slope * (x[0] - x3) - x[1]) % p

    return x3, y3






#Define cryptosystem: K = {(E, P, m, Q, n): Q = mP}
global a, b, p      #E function: f(x) = x^3 + a*x + b (mod p)
global P            #P generated point (is a public key): P = (x_p, y_p)
global m            #m  (is a private key)
global Q            #Q (is a public key): Q = (x_q, y_q)
global n            #n (is a public key)

#E setup
a = -3
b = 0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1
p = (pow(2, 192) - pow(2, 64) - 1)


#P setup
P = (0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012, 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811)

#m setup
m = 87686

#Q setup
Q = multiply(m, P)

#n setup
n = 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831

O = 'Origin'