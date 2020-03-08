#!/usr/bin/python
# -*- coding: UTF-8 -*-
from translate import google_translate
from translate import baidu_translate
from translate import bing_translate
from translate import iciba_translate


def translate(source_str):
    target_str = google_translate.google_translate(source_str)
    if target_str is None:
        target_str = bing_translate.bing_translate(source_str)
    if target_str is None:
        target_str = baidu_translate.baidu_translate(source_str)
    if target_str is None:
        target_str = iciba_translate.iciba_translate(source_str)
    if target_str is None:
        print("居然还是翻译失败了。")
        return None
    s = target_str + "(" + source_str + ")"
    print(s.replace("\\ ", "\\").replace("/ ", "/"))
    return s.replace("\\ ", "\\").replace("/ ", "/")
