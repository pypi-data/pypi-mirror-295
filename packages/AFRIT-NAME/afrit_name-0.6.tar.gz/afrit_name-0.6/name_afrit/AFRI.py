



from hashlib import md5
import ctypes
import json
import random
import requests
import time
from urllib.parse import urlparse, urlencode
from binascii        import hexlify
from uuid            import uuid4
from requests        import request
from AFRITON import AFRITON


import hashlib
import math


def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shitf(n, i):
    if n < 0:
        n = ctypes.c_uint32(n).value
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def decode(string):
    _0x50ff23 = {
        48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5,
        54: 6, 55: 7, 56: 8, 57: 9, 97: 10, 98: 11,
        99: 12, 100: 13, 101: 14, 102: 15
    }
    arr = []
    for i in range(0, 32, 2):
        arr.append(_0x50ff23[ord(string[i])] << 4 | _0x50ff23[ord(string[i + 1])])
    return arr


def md5_arry(arry):
    m = hashlib.md5()
    m.update(bytearray(arry))
    return m.hexdigest()


def md5_string(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()


def encodeWithKey(key, data):
    result = [None] * 256
    temp = 0
    output = ""
    for i in range(256):
        result[i] = i
    for i in range(256):
        temp = (temp + result[i] + key[i % len(key)]) % 256
        temp1 = result[i]
        result[i] = result[temp]
        result[temp] = temp1
    temp2 = 0
    temp = 0
    for i in range(len(data)):
        temp2 = (temp2 + 1) % 256
        temp = (temp + result[temp2]) % 256
        temp1 = result[temp2]
        result[temp2] = result[temp]
        result[temp] = temp1
        output += chr(ord(data[i]) ^ result[(result[temp2] + result[temp]) % 256])
    return output


def b64_encode(string, key_table="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="):
    last_list = list()
    for i in range(0, len(string), 3):
        try:
            num_1 = ord(string[i])
            num_2 = ord(string[i + 1])
            num_3 = ord(string[i + 2])
            arr_1 = num_1 >> 2
            arr_2 = ((3 & num_1) << 4 | (num_2 >> 4))
            arr_3 = ((15 & num_2) << 2) | (num_3 >> 6)
            arr_4 = 63 & num_3
        except IndexError:
            arr_1 = num_1 >> 2
            arr_2 = ((3 & num_1) << 4) | 0
            arr_3 = 64
            arr_4 = 64
        last_list.append(arr_1)
        last_list.append(arr_2)
        last_list.append(arr_3)
        last_list.append(arr_4)
    return "".join([key_table[value] for value in last_list])


def cal_num_list(_num_list):
    new_num_list = []
    for x in [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
        new_num_list.append(_num_list[x - 1])
    return new_num_list


def _0x22a2b6(_0x59d7ab, _0x151cde, _0x1e0c94, _0x54aa83, _0x76d8ab, _0x550bdb, _0xb90041, _0x44b16d, _0x28659f,
              _0x252c2c, _0x365218, _0x48af11, _0x25e3db, _0x34084f, _0x4f0729, _0x46a34c, _0x1f67f1, _0x5cd529,
              _0x53097b):
    _0xa0a6ac = [0] * 19
    _0xa0a6ac[-0x1 * -0x2192 + 0x11b * 0x5 + -0x2719 * 0x1] = _0x59d7ab
    _0xa0a6ac[0x4a * 0x3 + -0x6d * 0xb + -0x1e9 * -0x2] = _0x365218
    _0xa0a6ac[-0x59f * -0x3 + -0x46c * -0x4 + -0x228b] = _0x151cde
    _0xa0a6ac[0x11a1 + 0xf3d * -0x1 + 0x3 * -0xcb] = _0x48af11
    _0xa0a6ac[-0x1 * -0xa37 + 0x13 * 0x173 + -0x25bc] = _0x1e0c94
    _0xa0a6ac[-0x4 * -0x59f + -0x669 * 0x4 + 0x32d] = _0x25e3db
    _0xa0a6ac[-0x1b42 + 0x10 * -0x24 + 0x1d88] = _0x54aa83
    _0xa0a6ac[0x2245 + 0x335 * 0x6 + -0x357c] = _0x34084f
    _0xa0a6ac[0x3fb + 0x18e1 + -0x1cd4] = _0x76d8ab
    _0xa0a6ac[0x3 * 0x7a + 0x1 * 0x53f + 0x154 * -0x5] = _0x4f0729
    _0xa0a6ac[0x25a * -0x9 + 0x11f6 + 0xa6 * 0x5] = _0x550bdb
    _0xa0a6ac[-0x1b * -0x147 + -0x21e9 * -0x1 + 0x445b * -0x1] = _0x46a34c
    _0xa0a6ac[-0x2f * 0xaf + 0x22f0 + -0x2c3] = _0xb90041
    _0xa0a6ac[0x2f * 0x16 + 0x17 * 0x19 + -0x63c] = _0x1f67f1
    _0xa0a6ac[-0x46a * 0x1 + 0xb * -0x97 + 0xaf5] = _0x44b16d
    _0xa0a6ac[0x47 * 0x4f + -0x8cb * -0x4 + -0x3906] = _0x5cd529
    _0xa0a6ac[-0x7 * 0x40e + 0xb8b + 0x10e7] = _0x28659f
    _0xa0a6ac[0x6f9 + 0x196b + 0x5 * -0x677] = _0x53097b
    _0xa0a6ac[-0xa78 + 0x1b89 + 0xe5 * -0x13] = _0x252c2c
    return ''.join([chr(x) for x in _0xa0a6ac])


def _0x263a8b(_0x2a0483):
    return "\u0002" + "ÿ" + _0x2a0483


def get_x_bogus(params, data, user_agent):
    s0 = md5_string(data)
    s1 = md5_string(params)
    s0_1 = md5_arry(decode(s0))
    s1_1 = md5_arry(decode(s1))
    d = encodeWithKey([0, 1, 12], user_agent)
    ua_str = b64_encode(d)
    ua_str_md5 = md5_string(ua_str)
    timestamp = int(time.time())
    canvas = 536919696
    salt_list = [timestamp, canvas, 64, 0, 1, 12, decode(s1_1)[-2], decode(s1_1)[-1], decode(s0_1)[-2],
                 decode(s0_1)[-1], decode(ua_str_md5)[-2], decode(ua_str_md5)[-1]]
    for x in [24, 16, 8, 0]:
        salt_list.append(salt_list[0] >> x & 255)
    for x in [24, 16, 8, 0]:
        salt_list.append(salt_list[1] >> x & 255)
    _tem = 64
    for x in salt_list[3:]:
        _tem = _tem ^ x
    salt_list.append(_tem)
    salt_list.append(255)
    num_list = cal_num_list(salt_list)
    short_str_2 = encodeWithKey([255], _0x22a2b6(*num_list))
    short_str_3 = _0x263a8b(short_str_2)
    x_b = b64_encode(short_str_3, "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe")
    return x_b


def random_k(unm):
    y = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    z = []
    for i in range(unm):
        z.append(random.choice(y))

    return ''.join(z)


def random_32():
    reut = 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'
    hex_t = '0123456789abcdef'
    reut_li = []
    for i in reut:
        if i == 'x':
            reut_li.append(random.choice(hex_t))
        else:
            reut_li.append(i)
    return ''.join(reut_li)


def int32(i):
    return int(0xFFFFFFFF & i)


def fixk(k):
    if len(k) < 4:
        k = k[:4]
        k.extend([0] * (4 - len(k)))
    return k

def mx(sum, y, z, p, e, k):
    tmp = (((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4)))
    tmp ^= ((sum ^ y) + (k[p & 3 ^ e] ^ z))
    return tmp


def toBinaryString(v, includeLength):
    length = len(v)
    n = length << 2
    if includeLength:
        m = v[length - 1]
        n -= 4
        if m < n - 3 or m > n:
            return None
        n = m
    for i in range(length):
        v[i] = chr(v[i] & 0xFF) + chr((v[i] >> 8) & 0xFF) + chr((v[i] >> 16) & 0xFF) + chr((v[i] >> 24) & 0xFF)
    result = ''.join(v)
    if includeLength:
        return result[:n]
    return result


def encryptUint32Array(v, k):
    DELTA = 2654435769
    length = len(v)
    n = length - 1
    y, z, sum, e, p, q = 0, 0, 0, 0, 0, 0
    z = v[n]
    sum = 0
    for q in range(int(6 + 52 / length)):
        sum = int32(sum + DELTA)
        e = int(sum >> 2) & 3
        for p in range(n):
            y = v[p + 1]
            z = v[p] = int32(v[p] + mx(sum, y, z, p, e, k))
        y = v[0]
        z = v[n] = int32(v[n] + mx(sum, y, z, n, e, k))
    return v


def decryptUint32Array(v, k):
    DELTA = 2654435769
    length = len(v)
    n = length - 1
    y, z, sum, e, p, q = 0, 0, int32(0), 0, 0, 0
    y = v[0]
    q = math.floor(6 + 52 / length)
    sum = int32(q * DELTA)
    while sum != 0:
        e = int32(sum >> 2 & 3)
        p = n
        while p > 0:
            z = v[p - 1]
            y = v[p] = int32(v[p] - mx(sum, y, z, p, e, k))
            p -= 1
        z = v[n]
        y = v[0] = int32(v[0] - mx(sum, y, z, 0, e, k))
        sum = int32(sum - DELTA)
    return v


def utf8DecodeShortString(bs, n):
    charCodes = []
    i = 0
    off = 0
    len_ = len(bs)
    while i < n and off < len_:
        unit = ord(bs[off])
        off += 1
        if unit < 0x80:
            charCodes.append(unit)
        elif 0xc2 <= unit < 0xe0 and off < len_:
            charCodes.append(((unit & 0x1F) << 6) | (ord(bs[off]) & 0x3F))
            off += 1
        elif 0xe0 <= unit < 0xf0 and off + 1 < len_:
            charCodes.append(((unit & 0x0F) << 12) |
                             ((ord(bs[off]) & 0x3F) << 6) |
                             (ord(bs[off + 1]) & 0x3F))
            off += 2
        elif 0xf0 <= unit < 0xf8 and off + 2 < len_:
            rune = (((unit & 0x07) << 18) |
                    ((ord(bs[off]) & 0x3F) << 12) |
                    ((ord(bs[off + 1]) & 0x3F) << 6) |
                    (ord(bs[off + 2]) & 0x3F)) - 0x10000
            if 0 <= rune <= 0xFFFFF:
                charCodes.append(((rune >> 10) & 0x03FF) | 0xD800)
                charCodes.append((rune & 0x03FF) | 0xDC00)
            else:
                raise ValueError('Character outside valid Unicode range: '
                                 + hex(rune))
            off += 3
        else:
            raise ValueError('Bad UTF-8 encoding 0x' + hex(unit))
        i += 1
    return ''.join(chr(code) for code in charCodes)


def utf8DecodeLongString(bs, n):
    buf = []
    char_codes = [0] * 0x8000
    i = off = 0
    len_bs = len(bs)
    while i < n and off < len_bs:
        unit = ord(bs[off])
        off += 1
        divide = unit >> 4
        if divide < 8:
            char_codes[i] = unit
        elif divide == 12 or divide == 13:
            if off < len_bs:
                char_codes[i] = ((unit & 0x1F) << 6) | (ord(bs[off]) & 0x3F)
                off += 1
            else:
                raise ValueError('Unfinished UTF-8 octet sequence')
        elif divide == 14:
            if off + 1 < len_bs:
                char_codes[i] = ((unit & 0x0F) << 12) | ((ord(bs[off]) & 0x3F) << 6) | (ord(bs[off + 1]) & 0x3F)
                off += 2
            else:
                raise ValueError('Unfinished UTF-8 octet sequence')
        elif divide == 15:
            if off + 2 < len_bs:
                rune = (((unit & 0x07) << 18) | ((ord(bs[off]) & 0x3F) << 12) | ((ord(bs[off + 1]) & 0x3F) << 6) | (
                            ord(bs[off + 2]) & 0x3F)) - 0x10000
                off += 3
                if 0 <= rune <= 0xFFFFF:
                    char_codes[i] = (((rune >> 10) & 0x03FF) | 0xD800)
                    i += 1
                    char_codes[i] = ((rune & 0x03FF) | 0xDC00)
                else:
                    raise ValueError('Character outside valid Unicode range: 0x' + hex(rune))
            else:
                raise ValueError('Unfinished UTF-8 octet sequence')
        else:
            raise ValueError('Bad UTF-8 encoding 0x' + hex(unit))
        if i >= 0x7FFF - 1:
            size = i + 1
            char_codes = char_codes[:size]
            buf.append(''.join([chr(c) for c in char_codes]))
            n -= size
            i = -1
        i += 1
    if i > 0:
        char_codes = char_codes[:i]
        buf.append(''.join([chr(c) for c in char_codes]))
    return ''.join(buf)


def utf8Decode(bs, n=None):
    if n is None or n < 0:
        n = len(bs)
    if n == 0:
        return ''
    if all(0 <= ord(c) <= 127 for c in bs) or not all(0 <= ord(c) <= 255 for c in bs):
        if n == len(bs):
            return bs
        return bs[:n]
    return utf8DecodeShortString(bs, n) if n < 0x7FFF else utf8DecodeLongString(bs, n)


def decrypt(data, key):
    if data is None or len(data) == 0:
        return data

    key = utf8Encode(key)

    return utf8Decode(
        toBinaryString(decryptUint32Array(toUint32Array(data, False), fixk(toUint32Array(key, False))), True))


def encrypt(data, key):
    if (data is None) or (len(data) == 0):
        return data
    data = utf8Encode(data)
    key = utf8Encode(key)
    return toBinaryString(
        encryptUint32Array(
            toUint32Array(data, True),
            fixk(toUint32Array(key, False))
        ),
        False
    )


def strData(x, y):
    b = [i for i in range(256)]
    c = 0
    d = ""
    for i in range(256):
        c = (c + b[i] + ord(x[i % len(x)])) % 256
        a = b[i]
        b[i] = b[c]
        b[c] = a
    e = 0
    c = 0
    for i in range(len(y)):
        e = (e + 1) % 256
        c = (c + b[e]) % 256
        a = b[e]
        b[e] = b[c]
        b[c] = a
        d += chr(ord(y[i]) ^ b[(b[e] + b[c]) % 256])
    return d


def bytes_to_string(a, b=None, c=None):
    d = 'Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe='
    e = '='
    if c:
        e = ''
    if b:
        d = b
    g = ''
    h = 0
    while len(a) >= h + 3:
        f = 0
        f = f | ord(a[h]) << 16
        f = f | ord(a[h + 1]) << 8
        f = f | ord(a[h + 2]) << 0
        g += d[(16515072 & f) >> 18]
        g += d[(258048 & f) >> 12]
        g += d[(4032 & f) >> 6]
        g += d[63 & f]
        h += 3
    if len(a) - h > 0:
        f = (255 & ord(a[h])) << 16 | (ord(a[h + 1]) << 8 if len(a) > h + 1 else 0)
        g += d[(16515072 & f) >> 18]
        g += d[(258048 & f) >> 12]
        g += d[(4032 & f) >> 6] if len(a) > h + 1 else e
        g += e
    return g


def bool_0_1(x):
    if x is None:
        return ''
    elif isinstance(x, bool):
        return '1' if x else '0'
    else:
        return x


def fromCharCode(value_typ):
    unc = ''
    for c in value_typ:
        unc += chr(c & 0xffff)

    return unc


def utf8Encode(str):
    if all(ord(c) < 128 for c in str):
        return str
    buf = []
    n = len(str)
    i = 0
    while i < n:
        codeUnit = ord(str[i])
        if codeUnit < 0x80:
            buf.append(str[i])
            i += 1
        elif codeUnit < 0x800:
            buf.append(chr(0xC0 | (codeUnit >> 6)))
            buf.append(chr(0x80 | (codeUnit & 0x3F)))
            i += 1
        elif codeUnit < 0xD800 or codeUnit > 0xDFFF:
            buf.append(chr(0xE0 | (codeUnit >> 12)))
            buf.append(chr(0x80 | ((codeUnit >> 6) & 0x3F)))
            buf.append(chr(0x80 | (codeUnit & 0x3F)))
            i += 1
        else:
            if i + 1 < n:
                nextCodeUnit = ord(str[i + 1])
                if codeUnit < 0xDC00 and 0xDC00 <= nextCodeUnit and nextCodeUnit <= 0xDFFF:
                    rune = (((codeUnit & 0x03FF) << 10) | (nextCodeUnit & 0x03FF)) + 0x010000
                    buf.append(chr(0xF0 | ((rune >> 18) & 0x3F)))
                    buf.append(chr(0x80 | ((rune >> 12) & 0x3F)))
                    buf.append(chr(0x80 | ((rune >> 6) & 0x3F)))
                    buf.append(chr(0x80 | (rune & 0x3F)))
                    i += 2
                    continue
            raise ValueError('Malformed string')
    return ''.join(buf)


def toUint32Array(bs, includeLength):
    length = len(bs)
    n = length >> 2
    if (length & 3) != 0:
        n += 1
    if includeLength:
        v = [0] * (n + 1)
        v[n] = length
    else:
        v = [0] * n
    for i in range(length):
        v[i >> 2] |= ord(bs[i]) << ((i & 3) << 3)
    return v


def bytes2string_1(a, b="", c=False):
    d = 'Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe'
    e = ''
    if c:
        e = ''
    if b:
        d = b
    g = ''
    h = 0
    while len(a) >= h + 3:
        f = 0
        f |= ord(a[h]) << 16
        f |= ord(a[h + 1]) << 8
        f |= ord(a[h + 2]) << 0
        g += d[(16515072 & f) >> 18]
        g += d[(258048 & f) >> 12]
        g += d[(4032 & f) >> 6]
        g += d[63 & f]
        h += 3
    if len(a) - h > 0:
        f = (255 & ord(a[h])) << 16
        if len(a) > h + 1:
            f |= (255 & ord(a[h + 1])) << 8
        g += d[(16515072 & f) >> 18]
        g += d[(258048 & f) >> 12]
        if len(a) > h + 1:
            g += d[(4032 & f) >> 6]
        else:
            g += e
        g += e
    return g


def douyin_xxbg_q_encrypt(obj, obj_2=None):
    if obj_2:
        j = 0
        for i in range(len(obj)):
            if obj[j]['p']:
                obj[j]['r'] = obj_2[j]
                j += 1
    temp_text = ''
    for arg in obj:
        temp_text += bool_0_1(arg['r']) + '^^'
    temp_text += str(int(time.time() * 1000))
    salt = random_32()
    temp_num = math.floor(ord(salt[3]) / 8) + ord(salt[3]) % 8
    key = salt[4:4 + temp_num]
    entrypt_byte = encrypt(temp_text, key) + salt
    res = bytes2string_1(entrypt_byte, 'Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe==')
    return res


def tiktok_mssdk_encode(value):
    b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-."
    k = random_k(4)
    q = encrypt(value, k)
    result = k + bytes2string_1(q, b64)
    return result


def encrypt_strData(text):
    key_num = random.randint(200, 256)
    temp = fromCharCode([65, key_num]) + strData(fromCharCode([key_num]), text)
    return bytes_to_string(temp)




def left_shift(x, y):
    return ctypes.c_int(x << y).value


def get_time():
    return str(int(time.time() * 1000))


class AFREncrypt:
    def __init__(self, user_agent):
        self.ua = user_agent
        self.href_hash = ""
        self.ua_hash = ""
        self.params_hash = ""
        self.fix_hash = 65599
        self.fix_bin = 8240
        self.fix_seq = 65521
        self.canvas_hash = 536919696
        # self.ctx = self.load_js()

    # def load_js(self):
    #     # with open("./DouyinRegisterDevice/app/jsFiles/websdk.js", mode="r", encoding="utf-8") as f:
    #     with open("./websdk.js", mode="r", encoding="utf-8") as f:
    #         ctx = execjs.compile(f.read())
    #     # 本地
    #     # with open("./jsFiles/websdk.js", mode="r", encoding="utf-8") as f:
    #     #     ctx = execjs.compile(f.read())
    #
    #     return ctx

    @staticmethod
    def move_char_calc(nor):
        if 0 <= nor < 26:
            char_at = nor + 65
        elif 26 <= nor < 52:
            char_at = nor + 71
        elif nor == 62 or nor == 63:
            char_at = nor - 17
        else:
            char_at = nor - 4
        return chr(char_at)

    @staticmethod
    def unsigned_right_shift(signed, i=0):
        shift = signed % 0x100000000
        return shift >> i

    def sdb_hash(self, string=None, sdb_value=0):
        for index, char in enumerate(string):
            if string.startswith("_02B4Z6wo00"):
                sdb_value = self.unsigned_right_shift((sdb_value * self.fix_hash) + ord(char))
            elif string.startswith("{"):
                if index in [0, 1]:
                    sdb_value = self.unsigned_right_shift((sdb_value * self.fix_hash) ^ ord(char))
                else:
                    sdb_value = self.unsigned_right_shift((sdb_value * self.fix_hash) + ord(char))
            else:
                sdb_value = self.unsigned_right_shift((sdb_value ^ ord(char)) * self.fix_hash)
        return sdb_value

    def char_to_signature(self, sequence_num):
        offsets = [24, 18, 12, 6, 0]
        string = ""
        for offset in offsets:
            nor = sequence_num >> offset & 63
            string += self.move_char_calc(nor)
        return string

    def href_sequence(self, url):
        timestamp = int(time.time())
        timestamp_hash = self.sdb_hash(str(timestamp))
        self.href_hash = self.sdb_hash(url.split("//")[-1], sdb_value=timestamp_hash)
        sequence = timestamp ^ (self.href_hash % self.fix_seq * self.fix_seq)
        sequence = self.unsigned_right_shift(sequence)
        str_bin_sequence = str(bin(sequence)).replace("0b", "")
        fix_zero = "0" * (32 - len(str_bin_sequence))
        binary = f"{bin(self.fix_bin)}{fix_zero}{str_bin_sequence}".replace("0b", "")
        sequence_number = int(binary, 2)
        return sequence_number

    def char_to_signature1(self, sequence):
        sequence_first = sequence >> 2
        signature_one = self.char_to_signature(sequence_first)
        return signature_one

    def char_to_signature2(self, sequence):
        sequence_second = (sequence << 28) ^ (self.fix_bin >> 4)
        signature_two = self.char_to_signature(sequence_second)
        return signature_two

    def char_to_signature3(self, sequence):
        timestamp_sequence = sequence ^ self.canvas_hash
        sequence_three = left_shift(self.fix_bin, 26) ^ self.unsigned_right_shift(timestamp_sequence, i=6)
        signature_three = self.char_to_signature(sequence_three)
        return signature_three

    def char_to_signature4(self, sequence):
        timestamp_sequence = sequence ^ self.canvas_hash
        signature_four = self.move_char_calc(timestamp_sequence & 63)
        return signature_four

    def char_to_signature5(self, sequence, params, body=None):
        if body:
            new_body = dict()
            for key in sorted(body):
                new_body[key] = body[key]
            body_str = json.dumps(new_body, ensure_ascii=False).replace(" ", "")
            body_hash = self.sdb_hash(body_str)
            params = f"body_hash={body_hash}&{params}"
        sdb_sequence = self.sdb_hash(str(sequence))
        self.ua_hash = self.sdb_hash(self.ua, sdb_sequence)
        self.params_hash = self.sdb_hash(params, sdb_sequence)
        sequence_five = (((self.ua_hash % self.fix_seq) << 16) ^ (self.params_hash % self.fix_seq)) >> 2
        signature_five = self.char_to_signature(sequence_five)
        return signature_five

    def char_to_signature6(self, sequence):
        ua_remainder = self.ua_hash % self.fix_seq
        data_remainder = self.params_hash % self.fix_seq
        ua_data_number = ((int(ua_remainder) << 16) ^ int(data_remainder)) << 28
        sequence_six = ua_data_number ^ self.unsigned_right_shift((288 ^ sequence), 4)
        signature_six = self.char_to_signature(sequence_six)
        return signature_six

    def char_to_signature7(self):
        sequence_seven = self.href_hash % self.fix_seq
        signature_seven = self.char_to_signature(int(sequence_seven))
        return signature_seven

    def char_to_signature_hex(self, signature):
        sdb_signature = self.sdb_hash(signature)
        hex_signature = hex(sdb_signature).replace("0x", "")
        return hex_signature[-2:]

    def get_x_bogus(self, params, body=None, content_type=None):
        body_str = ""
        if content_type == "data":
            body_str = urlencode(body)
        elif content_type == "json":
            body_str = json.dumps(body, ensure_ascii=False).replace(" ", "")
        # x_bogus = self.ctx.call("get_xb", params, body_str, self.ua, self.canvas_hash)
        x_bogus = get_x_bogus(params, body_str, self.ua)
        return x_bogus

    def sign_100(self, ttscid):
        # sign = self.ctx.call("tiktok_mssdk_encode", ttscid)
        sign = tiktok_mssdk_encode(ttscid)
        return sign

    def generate_signature(self, href, api, body=None, content_type=None, ttscid="", prefix="_02B4Z6wo00001"):
        params = api.split("?")[1]
        params_str = str()
        if urlparse(api).query.split("&"):
            params_dict = {item.split("=")[0]: item.split("=")[1] for item in urlparse(api).query.split("&")}
            sort_dict = dict(sorted(params_dict.items(), key=lambda item: item[0]))
            for key, value in sort_dict.items():
                params_str += f"{key}={value}&"
        params_str += f"pathname={urlparse(api).path}&tt_webid=&uuid="
        x_bogus = self.get_x_bogus(params, body, content_type)
        params_str = f"X-Bogus={x_bogus}&{params_str}"
        sequence = self.href_sequence(href)
        sign1 = self.char_to_signature1(sequence)
        sign2 = self.char_to_signature2(sequence)
        sign3 = self.char_to_signature3(sequence)
        sign4 = self.char_to_signature4(sequence)
        sign5 = self.char_to_signature5(sequence, params_str, body)
        sign6 = self.char_to_signature6(sequence)
        sign7 = self.char_to_signature7()
        signature = f"{prefix}{sign1}{sign2}{sign3}{sign4}{sign5}{sign6}{sign7}"
        if ttscid:
            signature = f"{signature}{self.sign_100(ttscid)}"
        sign8 = self.char_to_signature_hex(signature)
        _signature = f"{signature}{sign8}"
        return x_bogus, _signature

    def cookie_signature(self, href, ac_nonce, ttscid="", prefix="_02B4Z6wo00f01"):
        sequence = self.href_sequence(href)
        sign1 = self.char_to_signature1(sequence)
        sign2 = self.char_to_signature2(sequence)
        sign3 = self.char_to_signature3(sequence)
        sign4 = self.char_to_signature4(sequence)
        sign5 = self.char_to_signature5(sequence, ac_nonce)
        sign6 = self.char_to_signature6(sequence)
        sign7 = self.char_to_signature7()
        signature = f"{prefix}{sign1}{sign2}{sign3}{sign4}{sign5}{sign6}{sign7}"
        sign8 = self.char_to_signature_hex(signature)
        if ttscid:
            _signature = f"{signature}{self.sign_100(ttscid)}{sign8}"
        else:
            _signature = f"{signature}{sign8}"
        return _signature

    def encrypt_strData(self, canvas_chrome_str):
        # strData = self.ctx.call("encrypt_strData", canvas_chrome_str)
        strData =encrypt_strData(canvas_chrome_str)
        return strData

    def ms_token(self, href):
        url = "https://mssdk.snssdk.com/web/report?msToken="
        canvas_chrome = {
            "tokenList": [],
            "navigator": {
                "appCodeName": self.ua.split("/")[0],
                "appMinorVersion": "undefined",
                "appName": "Netscape",
                "appVersion": self.ua.replace("Mozilla/", ""),
                "buildID": "undefined",
                "doNotTrack": "null",
                "msDoNotTrack": "undefined",
                "oscpu": "undefined",
                "platform": "Win32",
                "product": "Gecko",
                "productSub": "20030107",
                "cpuClass": "undefined",
                "vendor": "Google Inc.",
                "vendorSub": "",
                "deviceMemory": "8",
                "language": "zh-CN",
                "systemLanguage": "undefined",
                "userLanguage": "undefined",
                "webdriver": "false",
                "cookieEnabled": 1,
                "vibrate": 3,
                "credentials": 99,
                "storage": 99,
                "requestMediaKeySystemAccess": 3,
                "bluetooth": 99,
                "hardwareConcurrency": 4,
                "maxTouchPoints": -1,
                "languages": "zh-CN",
                "touchEvent": 2,
                "touchstart": 2,
            },
            "wID": {
                "load": 0,
                "nativeLength": 33,
                "jsFontsList": "17f",
                "syntaxError": "Failed to construct WebSocket: The URL Create WebSocket is invalid.",
                "timestamp": get_time(),
                "timezone": 8,
                "magic": 3,
                "canvas": str(self.canvas_hash),
                "wProps": 374198,
                "dProps": 2,
                "jsv": "1.7",
                "browserType": 16,
                "iframe": 2,
                "aid": 6383,
                "msgType": 1,
                "privacyMode": 0,
                "aidList": [6383, 6383, 6383],
                "index": 1,
            },
            "window": {
                "Image": 3,
                "isSecureContext": 1,
                "ActiveXObject": 4,
                "toolbar": 99,
                "locationbar": 99,
                "external": 99,
                "mozRTCPeerConnection": 4,
                "postMessage": 3,
                "webkitRequestAnimationFrame": 3,
                "BluetoothUUID": 3,
                "netscape": 4,
                "localStorage": 99,
                "sessionStorage": 99,
                "indexDB": 4,
                "devicePixelRatio": 1,
                "location": href,
            },
            "webgl": {
                "antialias": 1,
                "blueBits": 8,
                "depthBits": 24,
                "greenBits": 8,
                "maxAnisotropy": 16,
                "maxCombinedTextureImageUnits": 32,
                "maxCubeMapTextureSize": 16384,
                "maxFragmentUniformVectors": 1024,
                "maxRenderbufferSize": 16384,
                "maxTextureImageUnits": 16,
                "maxTextureSize": 16384,
                "maxVaryingVectors": 30,
                "maxVertexAttribs": 16,
                "maxVertexTextureImageUnits": 16,
                "maxVertexUniformVectors": 4096,
                "shadingLanguageVersion": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
                "stencilBits": 0,
                "version": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
                "vendor": "Google Inc. (Intel)",
                "renderer": "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            },
            "document": {
                "characterSet": "UTF-8",
                "compatMode": "CSS1Compat",
                "documentMode": "undefined",
                "layers": 4,
                "all": 12,
                "images": 99,
            },
            "screen": {
                "innerWidth": random.randint(1200, 1600),
                "innerHeight": random.randint(600, 800),
                "outerWidth": random.randint(1200, 1600),
                "outerHeight": random.randint(600, 800),
                "screenX": 0,
                "screenY": 0,
                "pageXOffset": 0,
                "pageYOffset": 0,
                "availWidth": random.randint(1200, 1600),
                "availHeight": random.randint(600, 800),
                "sizeWidth": random.randint(1200, 1600),
                "sizeHeight": random.randint(600, 800),
                "clientWidth": random.randint(1200, 1600),
                "clientHeight": random.randint(600, 800),
                "colorDepth": 24,
                "pixelDepth": 24,
            },
            "plugins": {
                "plugin": [
                    "internal-pdf-viewer|application/pdf|pdf",
                    "internal-pdf-viewer|text/pdf|pdf",
                    "internal-pdf-viewer|application/pdf|pdf",
                    "internal-pdf-viewer|text/pdf|pdf",
                    "internal-pdf-viewer|application/pdf|pdf",
                    "internal-pdf-viewer|text/pdf|pdf",
                    "internal-pdf-viewer|application/pdf|pdf",
                    "internal-pdf-viewer|text/pdf|pdf",
                    "internal-pdf-viewer|application/pdf|pdf",
                    "internal-pdf-viewer|text/pdf|pdf",
                ],
                "pv": "0",
            },
            "custom": {},
        }
        str_data = self.encrypt_strData(json.dumps(canvas_chrome).replace(" ", ""))
        payload = {
            "dataType": 8,
            "magic": 538969122,
            "strData": str_data,
            "tspFromClient": int(get_time()),
            "version": 1,
        }
        x_bogus = self.get_x_bogus(url.split("?")[-1], payload, content_type="json")
        url = url + "&X-Bogus=" + x_bogus
        headers = {"user-agent": self.ua}
        response = requests.post(url, json=payload, headers=headers)
        return response.cookies.get("msToken")

    def get_info(self, url):
        api = "https://xxbg.snssdk.com/websdk/v1/getInfo?"
        startTime = int(time.time() * 1000)
        timestamp1 = startTime + random.randint(1, 3)
        timestamp2 = timestamp1 + random.randint(10, 15)
        timestamp3 = timestamp2 + random.randint(100, 150)
        timestamp4 = timestamp3 + random.randint(1, 10)
        plain_arr_1 = [
            {"n": "aid", "f": 4, "r": 6383},
            {"n": "startTime", "f": 3, "r": startTime},
            {"n": "abilities", "f": 3, "r": "111"},
            {"n": "canvas", "f": 3, "r": self.canvas_hash},
            {"n": "timestamp1", "f": 3, "r": timestamp1},
            {"n": "platform", "f": 0, "r": "Win32"},
            {"n": "hardwareConcurrency", "f": 0, "r": 4},
            {"n": "deviceMemory", "f": 0, "r": 8},
            {"n": "language", "f": 0, "r": "zh-CN"},
            {"n": "languages", "f": 0,
             "r": random.sample(['zh-CN', 'zh-TW', 'zh', 'en-US', 'en', 'zh-HK', 'ja'], random.randint(1, 7))},
            {"n": "resolution", "f": 3, "r": f"{random.randint(1200, 1600)}_{random.randint(600, 800)}_24"},
            {"n": "availResolution", "f": 3, "r": f"{random.randint(1200, 1600)}_{random.randint(600, 800)}"},
            {"n": "screenTop", "f": 1, "r": 0},
            {"n": "screenLeft", "f": 1, "r": 0},
            {"n": "devicePixelRatio", "f": 1, "r": 1.25},
            {"n": "productSub", "f": 0, "r": "20030107"},
            {"n": "battery", "f": 3, "p": 1, "r": "true_0_Infinity_1"},
            {"n": "touchInfo", "f": 3, "r": "0_false_false"},
            {"n": "timezone", "f": 3, "r": 480},
            {"n": "timestamp2", "f": 3, "r": timestamp2},
            {
                "n": "gpuInfo",
                "f": 3,
                "r": "Google Inc. (Intel)/ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            },
            {"n": "jsFontsList", "f": 3, "r": "17f"},
            {
                "n": "pluginsList",
                "f": 3,
                "r": "PDF Viewerinternal-pdf-viewerapplication/pdftext/pdf##Chrome PDF Viewerinternal-pdf-viewerapplication/pdftext/pdf##Chromium PDF Viewerinternal-pdf-viewerapplication/pdftext/pdf##Microsoft Edge PDF Viewerinternal-pdf-viewerapplication/pdftext/pdf##WebKit built-in PDFinternal-pdf-viewerapplication/pdftext/pdf",
            },
            {"n": "timestamp3", "f": 3, "r": timestamp3},
            {"n": "userAgent", "f": 0, "r": self.ua},
            {"n": "everCookie", "f": 3, "m": "tt_scid"},
            {
                "n": "syntaxError",
                "f": 3,
                "r": "Failed to construct 'WebSocket': The URL 'Create WebSocket' is invalid.",
            },
            {"n": "nativeLength", "f": 3, "r": 33},
            {"n": "rtcIP", "f": 3, "p": 1, "r": "58.19.72.31"},
            {"n": "location", "f": 1, "r": url},
            {"n": "fpVersion", "f": 4, "r": "2.11.0"},
            # {"n": "clientId", "f": 3, "r": self.ctx.call("random_32")},
            {"n": "clientId", "f": 3, "r": random_32()},
            {"n": "timestamp4", "f": 3, "r": timestamp4},
            {"n": "extendField", "f": 4},
        ]
        plain_arr_2 = ["true_0_Infinity_1", "58.19.72.31"]
        # q = self.ctx.call("douyin_xxbg_q_encrypt", plain_arr_1, plain_arr_2)
        q = douyin_xxbg_q_encrypt(plain_arr_1, plain_arr_2)

        headers = {"user-agent": self.ua}
        params = {"q": q, "callback": f"_7013_{get_time()}"}
        response = requests.get(api, headers=headers, params=params)
        return response.cookies

class Signer:
    shift_array = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe"
    magic = 536919696

    def md5_2x(string):
        return md5(md5(string.encode()).digest()).hexdigest()

    def rc4_encrypt(plaintext: str, key: list[int]) -> str:
        s_box = [_ for _ in range(256)]
        index = 0

        for _ in range(256):
            index = (index + s_box[_] + key[_ % len(key)]) % 256
            s_box[_], s_box[index] = s_box[index], s_box[_]

        _ = 0
        index = 0
        ciphertext = ""

        for char in plaintext:
            _ = (_ + 1) % 256
            index = (index + s_box[_]) % 256

            s_box[_], s_box[index] = s_box[index], s_box[_]
            keystream = s_box[(s_box[_] + s_box[index]) % 256]
            ciphertext += chr(ord(char) ^ keystream)

        return ciphertext

    def b64_encode(
        string,
        key_table="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    ):
        last_list = list()
        for i in range(0, len(string), 3):
            try:
                num_1 = ord(string[i])
                num_2 = ord(string[i + 1])
                num_3 = ord(string[i + 2])
                arr_1 = num_1 >> 2
                arr_2 = (3 & num_1) << 4 | (num_2 >> 4)
                arr_3 = ((15 & num_2) << 2) | (num_3 >> 6)
                arr_4 = 63 & num_3

            except IndexError:
                arr_1 = num_1 >> 2
                arr_2 = ((3 & num_1) << 4) | 0
                arr_3 = 64
                arr_4 = 64

            last_list.append(arr_1)
            last_list.append(arr_2)
            last_list.append(arr_3)
            last_list.append(arr_4)

        return "".join([key_table[value] for value in last_list])

    def filter(num_list: list):
        return [
            num_list[x - 1]
            for x in [3,5,7,9,11,13,15,17,19,21,4,6,8,10,12,14,16,18,20,
            ]
        ]

    def scramble(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s) -> str:
        return "".join(
            [
                chr(_)
                for _ in [a,k,b,l,c,m,d,n,e,o,f,p,g,q,h,r,i,s,j,
                ]
            ]
        )

    def checksum(salt_list: str) -> int:
        checksum = 64
        _ = [checksum := checksum ^ x for x in salt_list[3:]]

        return checksum

    def _x_bogus(params, user_agent, timestamp, data) -> str:

        md5_data = Signer.md5_2x(data)
        md5_params = Signer.md5_2x(params)
        md5_ua = md5(
            Signer.b64_encode(Signer.rc4_encrypt(user_agent, [0, 1, 14])).encode()
        ).hexdigest()

        salt_list = [
            timestamp,
            Signer.magic,
            64,
            0,
            1,
            14,
            bytes.fromhex(md5_params)[-2],
            bytes.fromhex(md5_params)[-1],
            bytes.fromhex(md5_data)[-2],
            bytes.fromhex(md5_data)[-1],
            bytes.fromhex(md5_ua)[-2],
            bytes.fromhex(md5_ua)[-1],
        ]

        salt_list.extend([(timestamp >> i) & 0xFF for i in range(24, -1, -8)])
        salt_list.extend([(salt_list[1] >> i) & 0xFF for i in range(24, -1, -8)])
        salt_list.extend([Signer.checksum(salt_list), 255])

        num_list = Signer.filter(salt_list)
        rc4_num_list = Signer.rc4_encrypt(Signer.scramble(*num_list), [255])

        return Signer.b64_encode(f"\x02ÿ{rc4_num_list}", Signer.shift_array)
    
def tim():
    _rticket = int(time.time() * 1000)
    ts=str(int(time.time() * 1000))[:10]
    ts1=str(int(time.time() * 1000))[:10]
    icket = int(time.time() * 1000)
    return _rticket,ts,ts1,icket



def tt_encrypt(data) -> str:
  return AFRITON().encrypt(json.dumps(data).replace(" ", ""))
def device_register() -> dict:
      _rticket,ts,ts1,icket=tim()
      openudid = hexlify(random.randbytes(8)).decode()
      cdid = str(uuid4())
      google_aid = str(uuid4())
      clientudid = str(uuid4())
      req_id = str(uuid4())
      url = f"https://log-va.tiktokv.com/service/2/device_register/?ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=170404&version_name=17.4.4&device_platform=android&ab_version=17.4.4&ssmix=a&device_type=SM-G611M&device_brand=samsung&language=en&os_api=28&os_version=9&openudid={openudid}&manifest_version_code=2021704040&resolution=720*1280&dpi=320&update_version_code=2021704040&_rticket={icket}&_rticket={_rticket}&storage_type=2&app_type=normal&sys_region=US&appTheme=light&pass-route=1&pass-region=1&timezone_name=Europe%252FBerlin&cpu_support64=false&host_abi=armeabi-v7a&app_language=en&ac2=wifi&uoo=1&op_region=US&timezone_offset=3600&build_number=17.4.4&locale=en&region=US&ts={ts}&cdid={cdid}"
      
      payload = {"magic_tag":"ss_app_log","header":{"display_name":"TikTok","update_version_code":2021704040,"manifest_version_code":2021704040,"app_version_minor":"","aid":1233,"channel":"googleplay","package":"com.zhiliaoapp.musically","app_version":"17.4.4","version_code":170404,"sdk_version":"2.12.1-rc.5","sdk_target_version":29,"git_hash":"050d489d","os":"Android","os_version":"9","os_api":28,"device_model":"SM-G611M","device_brand":"samsung","device_manufacturer":"samsung","cpu_abi":"armeabi-v7a","release_build":"e1611c6_20200824","density_dpi":320,"display_density":"xhdpi","resolution":"1280x720","language":"en","timezone":1,"access":"wifi","not_request_sender":0,"mcc_mnc":"26203","rom":"G611MUBS6CTD1","rom_version":"PPR1.180610.011","cdid":cdid,"sig_hash":"e89b158e4bcf988ebd09eb83f5378e87","gaid_limited":0,"google_aid":google_aid,"openudid":openudid,"clientudid":clientudid,"region":"US","tz_name":"Europe\\/Berlin","tz_offset":7200,"oaid_may_support":False,"req_id":req_id,"apk_first_install_time":1653436407842,"is_system_app":0,"sdk_flavor":"global"},"_gen_time":1653464286461}
      
      headers = {
        "Host": "log-va.tiktokv.com",
        "accept-encoding": "gzip",
        "sdk-version": "2",
        "passport-sdk-version": "17",
        "content-type": "application/octet-stream",
        "user-agent": "okhttp/3.10.0.1"
      }
      response = request("POST", url, headers=headers, data=bytes.fromhex(tt_encrypt(payload))).json()
      print(response)
      try:
       install_id = response["install_id_str"]
       device_id = response["device_id_str"]
       ti=response['server_time']
       return install_id,device_id,openudid,cdid,ti
      except:
        install_id      = int(bin(int(time.time()) + random.randint(0, 100))[2:] + "10100110110100110000011100000101", 2)
        device_id      = int(bin(int(time.time()) + random.randint(0, 100))[2:] + "00101101010100010100011000000110", 2)
        openudid = hexlify(random.randbytes(8)).decode()
        cdid = str(uuid4())
        ti=str(int(time.time() * 1000))[:10]
        return install_id,device_id,openudid,cdid,ti


class Xgorgon:
    def __init__(self, params: str, data: str) -> None:

        self.params = params
        self.data = data
        self.cookies = None

    def hash(self, data: str) -> str:
        _hash = str(hashlib.md5(data.encode()).hexdigest())

        return _hash

    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = (
            base_str + self.hash(self.data) if self.data else base_str + str("0" * 32)
        )
        base_str = (
            base_str + self.hash(self.cookies)
            if self.cookies
            else base_str + str("0" * 32)
        )

        return base_str

    def get_value(self) -> json:
        base_str = self.get_base_string()

        return self.encrypt(base_str)

    def encrypt(self, data: str) -> json:
        unix = int(time.time())
        len = 0x14
        key = [
            0xDF,
            0x77,
            0xB9,
            0x40,
            0xB9,
            0x9B,
            0x84,
            0x83,
            0xD1,
            0xB9,
            0xCB,
            0xD1,
            0xF7,
            0xC2,
            0xB9,
            0x85,
            0xC3,
            0xD0,
            0xFB,
            0xC3,
        ]
        param_list = []
        for i in range(0, 12, 4):
            temp = data[8 * i : 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2 : (j + 1) * 2], 16)
                param_list.append(H)

        param_list.extend([0x0, 0x6, 0xB, 0x1C])

        H = int(hex(unix), 16)

        param_list.append((H & 0xFF000000) >> 24)
        param_list.append((H & 0x00FF0000) >> 16)
        param_list.append((H & 0x0000FF00) >> 8)
        param_list.append((H & 0x000000FF) >> 0)

        eor_result_list = []

        for A, B in zip(param_list, key):
            eor_result_list.append(A ^ B)

        for i in range(len):

            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len]
            E = C ^ D

            F = self.rbit_algorithm(E)
            H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
            eor_result_list[i] = H

        result = ""
        for param in eor_result_list:
            result += self.hex_string(param)

        return {"X-Gorgon": ("0404b0d30000" + result), "X-Khronos": str(unix)}
    def rbit_algorithm(self, num):
        result = ""
        tmp_string = bin(num)[2:]

        while len(tmp_string) < 8:
            tmp_string = "0" + tmp_string

        for i in range(0, 8):
            result = result + tmp_string[7 - i]

        return int(result, 2)

    def hex_string(self, num):
        tmp_string = hex(num)[2:]

        if len(tmp_string) < 2:
            tmp_string = "0" + tmp_string

        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num)

        return int(tmp_string[1:] + tmp_string[:1], 16)