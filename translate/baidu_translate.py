# -*- coding: utf-8 -*-
import requests
import re
import math


def rl(r, o):
    for t in range(0, len(o) - 2, 3):
        a = o[t + 2]
        if a >= 'a':
            a = ord(a[0]) - 87
        else:
            a = int(a)
        if "+" == o[t + 1]:
            a = r >> a
        else:
            a = r << a
        if "+" == o[t]:
            r = r + a & 4294967295
        else:
            r = r ^ a
    return r


def token(a, gtk):
    o = len(a)
    if o > 30:
        a = "" + a[0: 0 + 10] + a[math.floor(o / 2) - 5:math.floor(o / 2) + 5] + a[len(a) - 10:len(a)]
    t = ""
    C = None
    if C != None:
        t = C
    else:
        if gtk != None:
            C = gtk
        else:
            C = ""
        t = C

    e = t.split(".")
    h = int(e[0]) or 0
    i = int(e[1]) or 0

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
    a = h
    for f in range(len(e)):
        a += e[f]
        a = rl(a, sb)
    a = rl(a, Zb)
    a ^= i
    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a %= 1E6
    return str(a).split(".")[0] + jd + str(int(a) ^ h)


class Dict:
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.token = None
        self.gtk = None

        # 获得token和gtk
        # 必须要加载两次保证token是最新的，否则会出现998的错误
        self.get_token_gtk()
        self.get_token_gtk()

    def get_token_gtk(self):
        url = 'https://fanyi.baidu.com'
        try:
            r = self.sess.get(url, headers=self.headers, timeout=5)
            self.token = re.findall(r"token: '(.*?)',", r.text)[0]
            self.gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[0]
        except Exception as e:
            raise e

    def langdetect(self, query):
        url = 'https://fanyi.baidu.com/langdetect'
        data = {'query': query}
        try:
            r = self.sess.post(url=url, data=data, timeout=5)
        except Exception as e:
            raise e

        json = r.json()
        if 'msg' in json and json['msg'] == 'success':
            return json['lan']
        return None

    def translate(self, query, dst='zh', src=None):
        url = 'https://fanyi.baidu.com/v2transapi'

        sign = token(query, self.gtk)
        print(sign)

        if not src:
            src = self.langdetect(query)

        data = {
            'from': src,
            'to': dst,
            'query': query,
            'simple_means_flag': 3,
            'sign': sign,
            'token': self.token,
        }
        try:
            r = self.sess.post(url=url, data=data, timeout=5)
        except Exception as e:
            return None

        if r.status_code != 200:
            return None
        return r.json()['trans_result']['data'][0]['dst']


def baidu_translate(source_str):
    try:
        return Dict().translate(source_str)
    except Exception as e:
        print(e)
        return None
