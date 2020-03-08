#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests


def iciba_translate(source_str):
    append = False
    if len(source_str.split(" ")) == 1 or (len(source_str.split(" ")) == 2 and source_str.split(" ")[1] == ""):
        append = True
        source_str += "."
    try:
        target = requests.post("http://fy.iciba.com/ajax.php?a=fy", data={
            "f": "en",
            "t": "zh",
            "w": source_str
        }, params={
            "a": "fy"
        }, headers={
            "authority": "cn.bing.com",
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        })
    except Exception as e:
        print(e)
        return None
    if target.status_code != 200:
        print(target.status_code)
        return None
    target_str = target.json()['content']['out']
    if append:
        target_str = target_str.replace("。", "").replace(" ", "")
    return target_str
