#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

from translate import google_translate
from translate import baidu_translate
from translate import bing_translate
from translate import iciba_translate


class Translate:
    def __init__(self):
        self.translate_vendor = 0
        self.try_count = 0

    def translate(self, source_str):
        if self.translate_vendor == 0:
            print("尝试使用Google翻译:" + source_str + "...")
            target_str = google_translate.google_translate(source_str)
        elif self.translate_vendor == 1:
            print("尝试使用百度翻译:" + source_str + "...")
            target_str = baidu_translate.baidu_translate(source_str)
        # elif self.translate_vendor == 1:
        #     print("尝试使用Bing翻译:" + source_str + "...")
        #     target_str = bing_translate.bing_translate(source_str)
        else:
            print("尝试使用金山翻译:" + source_str + "...")
            target_str = iciba_translate.iciba_translate(source_str)
        if target_str is None:
            self.translate_vendor = self.translate_vendor + 1
            self.try_count = self.try_count + 1
            # if self.try_count >= 4:
            if self.try_count >= 3:
                # print("尝试了四个API.居然还是翻译失败了。")
                print("尝试了三个API.居然还是翻译失败了。")
                return None
            return self.translate(source_str)
        else:
            self.try_count = 0
            s = target_str + "(" + source_str + ")"
            print(s.replace("\\ ", "\\").replace("/ ", "/"))
            return s.replace("\\ ", "\\").replace("/ ", "/")
