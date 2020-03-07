#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests


def rl(a, b):
    t = "a"
    Yb = "+"
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        if d >= t:
            d = ord(d[0]) - 87
        else:
            d = int(d)
        if b[c + 1] == Yb:
            d = a >> d
        else:
            d = a << d

        if b[c] == Yb:
            a = a + d & 4294967295
        else:
            a = a ^ d
    return a


def token(a):
    k = ""
    b = 406644
    b1 = 3293161072

    jd = "."
    sb = "+-a^+6"
    Zb = "+-3^+b+-f"
    e = []
    for g in range(len(a)):
        m = ord(a[g])
        if 128 > m:
            e.append(m)
        else:
            if 2048 > m:
                e.append(m >> 6 | 192)
            else:
                if 55296 == (m & 64512) and g + 1 < a.length and 56320 == (ord(a[g + 1]) & 64512):
                    g = g + 1
                    m = 65536 + ((m & 1023) << 10) + (ord(a[g]) & 1023)
                    e.append(m >> 18 | 240)
                    e.append(m >> 12 & 63 | 128)
                else:
                    e.append(m >> 12 | 224)
                    e.append(m >> 6 & 63 | 128)
                    e.append(m & 63 | 128)
    a = b
    for f in range(len(e)):
        a += e[f]
        a = rl(a, sb)
    a = rl(a, Zb)
    a ^= b1 or 0
    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a %= 1E6
    return str(a).split(".")[0] + jd + str(int(a) ^ b)


def translate(source_str):
    tk = token(source_str)
    target_str = requests.get("https://translate.google.cn/translate_a/t", params={
        "client": "webapp",
        "sl": "auto",
        "tl": "zh-CN",
        "tk": tk,
        "q": source_str
    }, headers={
        "authority": "translate.google.cn",
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Host": "translate.google.cn"
    })
    s = target_str.json()[0] + "(" + source_str + ")"
    print(s.replace("\\ ", "\\"))
    return s