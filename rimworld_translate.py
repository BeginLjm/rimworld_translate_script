#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import codecs
import time

from translate import translate

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

[
    {
        "name": "a",
        "languages": [
            {
                "path": "a",
                "type": 0,  # 0.正常 1.异常
                "keys": [
                    {
                        "key": "key",
                        "en": "en_value",
                        "zh": "zh_value"
                    }
                ]
            }
        ]
    }
]


class RimWorldTranslate:
    def __init__(self):
        self.translate = translate.Translate()

    def read_xml_file(self, path):
        language = {}
        language["path"] = path
        print(path)
        try:
            parser = et.parse(path)
            language["type"] = 0
            language["keys"] = []
            for child in parser.getroot():
                language["keys"].append({"key": child.tag, "en": child.text})
        except et.ParseError:
            language["type"] = 1
        finally:
            return language

    def list_all_xml_files(self, rootdir):
        _files = []
        list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(rootdir, list[i])
            if os.path.isdir(path):
                _files.extend(self.list_all_xml_files(path))
            if os.path.isfile(path) and path.endswith(".xml"):
                _files.append(path)
        return _files

    def find_need_translate_list(self, root_path):
        mod_number_list = os.listdir(path)
        _list = []
        for mod_number in mod_number_list:
            zh_cn = os.path.exists(path + os.sep + mod_number + os.sep + "Languages" + os.sep + "ChineseSimplified")
            zh_tw = os.path.exists(path + os.sep + mod_number + os.sep + "Languages" + os.sep + "ChineseTraditional")
            en = os.path.exists(path + os.sep + mod_number + os.sep + "Languages" + os.sep + "English")
            if zh_cn == False and zh_tw == False and en == True:
                _list.append(root_path + os.sep + mod_number)
        return _list

    def find_mod_name(self, mod_path):
        parser = et.parse(mod_path)
        return parser.getroot().find("name").text

    def find_mod_languages_list_json(self, mod_path):
        mod_list = self.find_need_translate_list(mod_path)
        mod_list_json = []
        for mod in mod_list:
            mod_map = {}
            mod_map["name"] = self.find_mod_name(mod + os.sep + "About" + os.sep + "About.xml")
            mod_languages = []
            for language in self.list_all_xml_files(mod + os.sep + "Languages" + os.sep + "English"):
                mod_languages.append(self.read_xml_file(language))
            mod_map["languages"] = mod_languages
            mod_list_json.append(mod_map)

        return mod_list_json

    def output_zh_file(self, mod_list):
        for mod in mod_list:
            for language in mod['languages']:
                if language['type'] == 1:
                    continue
                self.create_xml_file(language)

    def create_xml_file(self, language):
        import xml.dom.minidom

        # 在内存中创建一个空的文档
        doc = xml.dom.minidom.Document()
        # 创建一个根节点Managers对象
        root = doc.createElement('LanguageData')
        # 将根节点添加到文档对象中
        doc.appendChild(root)

        for key in language['keys']:
            k = doc.createElement(key['key'])
            k.appendChild(doc.createTextNode(str(key['zh_CN'])))
            root.appendChild(k)
        # 开始写xml文档
        path = language['path'].replace('English', 'ChineseSimplified')
        dir = path.replace(path.split(os.sep)[len(path.split(os.sep)) - 1], "")
        if not os.path.exists(dir):
            os.makedirs(dir)
        fp = codecs.open(path, 'w', encoding='utf-8')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        fp.close()
        print(dir)
        print(path)

    def translate_mod_list(self, mod_list):
        for mod in mod_list:
            print(mod['name'] + " 开始翻译.是否开始翻译(Y/N/S) (输入Y开始翻译，输入N结束，输入S跳过当前mod)")
            y = input()
            if y == 'Y' or y == 'y':
                for language in mod['languages']:
                    if language['type'] == 1:
                        continue
                    for key in language['keys']:
                        if key['en'] is not None:
                            zh = self.translate.translate(key['en'])
                            time.sleep(1)
                            if zh is None:
                                print(mod['name'] + " 翻译失败，终止翻译。")
                                return mod_list
                            else:
                                key['zh_CN'] = zh
                        else:
                            key['zh_CN'] = " "
                    self.create_xml_file(language)
                print(mod['name'] + " 已翻译完成")
            elif y == 's' or y == 'S':
                continue
            else:
                break
        return mod_list


if __name__ == '__main__':
    print("请输入Mod列表路径：")
    path = input()
    # path = "/Users/lujunming/Library/Application Support/Steam/steamapps/workshop/content/294100"
    # path = "/Users/lujunming/Library/Application Support/Steam/steamapps/common/RimWorld/RimWorldMac.app/Mods"
    rimworld_translate = RimWorldTranslate()
    mod_json = rimworld_translate.find_mod_languages_list_json(path)
    print("找到" + str(len(mod_json)) + "个Mod不包含中文资源,是否开始翻译.(Y/N) (输入Y开始翻译，输入N结束)")
    y = input()
    if y == 'Y' or y == 'y':
        if len(mod_json) > 0:
            mod_json = rimworld_translate.translate_mod_list(mod_json)
            # output_zh_file(mod_json)
        output = codecs.open(path + os.sep + "auto_translate.json", 'w', encoding='utf-8')
        output.write(json.dumps(mod_json))
        output.close()
    print("翻译结束")
