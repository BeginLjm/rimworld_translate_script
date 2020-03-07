#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import codecs
import google_translate

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


def read_xml_file(path):
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


def list_all_xml_files(rootdir):
    _files = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isdir(path):
            _files.extend(list_all_xml_files(path))
        if os.path.isfile(path) and path.endswith(".xml"):
            _files.append(path)
    return _files


def find_need_translate_list(root_path):
    mod_number_list = os.listdir(path)
    _list = []
    for mod_number in mod_number_list:
        zh_cn = os.path.exists(path + os.sep + mod_number + os.sep + "Languages" + os.sep + "ChineseSimplified")
        zh_tw = os.path.exists(path + os.sep + mod_number + os.sep + "Languages" + os.sep + "ChineseTraditional")
        en = os.path.exists(path + os.sep + mod_number + os.sep + "Languages" + os.sep + "English")
        if zh_cn == False and zh_tw == False and en == True:
            _list.append(root_path + os.sep + mod_number)
    return _list


def find_mod_name(mod_path):
    parser = et.parse(mod_path)
    return parser.getroot().find("name").text


def find_mod_languages_list_json(mod_path):
    mod_list = find_need_translate_list(mod_path)
    mod_list_json = []
    for mod in mod_list:
        mod_map = {}
        mod_map["name"] = find_mod_name(mod + os.sep + "About" + os.sep + "About.xml")
        mod_languages = []
        for language in list_all_xml_files(mod + os.sep + "Languages" + os.sep + "English"):
            mod_languages.append(read_xml_file(language))
        mod_map["languages"] = mod_languages
        mod_list_json.append(mod_map)

    return mod_list_json


def translate_mod_list(mod_list):
    for mod in mod_list:
        for language in mod['languages']:
            if language['type'] == 1:
                continue
            for key in language['keys']:
                if key['en'] is not None:
                    key['zh_CN'] = google_translate.translate(key['en'])
                else:
                    key['zh_CN'] = " "
    return mod_list


def output_zh_file(mod_list):
    for mod in mod_list:
        for language in mod['languages']:
            if language['type'] == 1:
                continue
            create_xml_file(language)


def create_xml_file(language):
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


if __name__ == '__main__':
    print("请输入Mod列表路径：")
    path = input()
    # path = "/Users/lujunming/Library/Application Support/Steam/steamapps/workshop/content/294100"
    # path = "/Users/lujunming/Library/Application Support/Steam/steamapps/common/RimWorld/RimWorldMac.app/Mods"
    mod_json = find_mod_languages_list_json(path)
    print(mod_json)
    if len(mod_json) > 0:
        mod_json = translate_mod_list(mod_json)
        output_zh_file(mod_json)
    output = codecs.open(path + os.sep + "auto_translate.json", 'w', encoding='utf-8')
    output.write(json.dumps(mod_json))
    output.close()
