#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests


def bing_translate(source_str):
    try:
        target = requests.post("https://cn.bing.com/ttranslatev3", data={
            "fromLang": "auto-detect",
            "text": source_str,
            "to": "zh-Hans"
        }, params={
            "isVertical": 1,
            "IG": "B9BD22583791491DA32C5EEF137BF05D",
            "IID": "translator.5028.1"
        }, headers={
            "authority": "cn.bing.com",
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        })
    except Exception as e:
        return None
    if target.status_code != 200:
        return None
    target_str = target.json()[0]['translations'][0]['text']
    return target_str
