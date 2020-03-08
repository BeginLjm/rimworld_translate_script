# RimWorld mod 自动机翻脚本

**！！！使用前一定要注意备份mod文件夹，避免数据损坏。！！！**

## 简介
这是一个很简单的RimWorld mod机翻脚本，使用的Google翻译。翻译后会保留原文，展示形式为<u>**中文(English)**</u>

## 使用方式
### Windows
1. 下载脚本
    1. 直接点击网页上方绿色按钮<u>**clone or download**</u>后点击<u>**download zip**</u>
    2. 解压缩
2. 下载安装 Python3
    1. 打开网页 https://www.python.org/downloads/ 
    2. 点击<u>**Download Python 3.x.x**</u>
    3. 下载完成后双击打开
    4. **勾选上Add Python 3.x to PATH**
    5. 点击Install Now
3. 安装依赖
    1. 右键电脑右下角Windows图标点击运行，输入CMD，确定
    2. 在CMD窗口中输入`pip3 install requests` 回车执行。
4. 开始翻译
    1. 在CMD窗口中输入`python `注意有空格
    2. 将解压出的文件中的rimworld_translate.py拖入CMD窗口 回车执行
    3. 输入mod文件的上层目录，就是包含所有mod文件夹的目录
4. Mod顺序调整。**注意需要将自己原本订阅的汉化mod放在原mod之前。就能做到补充翻译的能力，否则机翻会覆盖汉化mod。**

## 效果展示
### 汉化效果
![效果展示](https://github.com/BeginLjm/rimworld_translate_script/raw/master/image/image-1.png "效果展示")
### 补充汉化效果
![补充汉化效果](https://github.com/BeginLjm/rimworld_translate_script/raw/master/image/image-2.jpg "补充汉化效果")

## 常见问题
1. pip3 install后一直没反应，之后出现Timout。答：科学上网
2. 脚本执行后报错“连接尝试失败”。答：科学上线
3. 报错“系统找不到路径”。答：确认下输入的mod列表路径是否正确
4. 翻译的看不懂。答：毕竟是机翻，所以保留了英文原文以供参考

## 更新日志
2020-03-08
1. 加入百度、Bing、金山翻译提高翻译稳定性

2020-03-07
1. 更换翻译方式不再依赖googletrans库，提高翻译成功绿
2. 加入跳过mod翻译功能。
3. 修改写入文件逻辑，翻译完成一个mod后直接写入，避免网络抖动导致白等半天。hhh
