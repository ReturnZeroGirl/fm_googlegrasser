import threading
import random
import time
import configparser
from datetime import datetime
from deep_translator import *
import logging
import colorlog
import os


logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置日志记录器级别
formatter = colorlog.ColoredFormatter(
    "%(log_color)s [%(asctime)s] (%(threadName)s) -%(levelname)s- %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)
fileformatter = colorlog.ColoredFormatter(
    "%(log_color)s [%(asctime)s] (%(threadName)s) -%(levelname)s- %(message)s",
)
# 创建控制台处理器并设置级别
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d,%H-%M-%S")
file_handler = logging.FileHandler("logs/"+str(formatted_time)+".log",encoding="utf-8",mode="w+")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(fileformatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
if not os.path.exists("logs"):
    # 如果不存在，创建文件夹
    try:
        os.makedirs("logs")
    except Exception as e:
        logger.critical("无法创建目录 logs")
        raise SystemExit
    logger.info("已创建目录 logs")
else:
    logger.info("logs 目录已存在")
config = configparser.ConfigParser()
config.read("config.ini")
logger.info("配置文件读取成功")
enc = config["options"]["encoding"]
languages = ['af', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bm', 'eu', 'be', 'bn', 'bho', 'bs', 'bg', 'ca', 'ceb',
             'ny', 'zh-CN', 'zh-TW', 'co', 'hr', 'cs', 'da', 'dv', 'doi', 'nl', 'en', 'eo', 'et', 'ee', 'tl', 'fi',
             'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig',
             'ilo', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'rw', 'gom', 'ko', 'kri', 'ku', 'ckb', 'ky', 'lo',
             'la', 'lv', 'ln', 'lt', 'lg', 'lb', 'mk', 'mai', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mni-Mtei', 'lus',
             'mn', 'my', 'ne', 'no', 'or', 'om', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa', 'gd',
             'nso', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te',
             'th', 'ti', 'ts', 'tr', 'tk', 'ak', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']
langdict = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as',
            'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn',
            'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny',
            'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr',
            'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en',
            'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr',
            'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn',
            'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi',
            'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id',
            'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk',
            'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri',
            'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la',
            'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb',
            'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt',
            'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn',
            'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps',
            'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro',
            'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr',
            'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl',
            'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg',
            'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts',
            'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug',
            'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo',
            'zulu': 'zu'}


def shuffle_array(arr):
    n = len(arr)
    for i in range(n - 1, 0, -1):
        time.sleep(0.0001)
        # 生成一个随机索引
        j = random.randint(0, i)
        # 交换arr[i]和arr[j]
        arr[i], arr[j] = arr[j], arr[i]
    return arr


try:
    file = open(config["options"]["file_scr"], "a+", encoding=enc)
    logger.info("源文件读取成功")
except Exception as e:
    logger.error(e)
    logger.critical("源文件读取出错,请检查配置文件!")
    raise SystemExit

content_scr = []
content_out = {}


def translator_(freq, content, id):
    text = content
    for i in range(freq):
        targetlang = shuffle_array(languages)[0]
        while True:
            try:
                text = GoogleTranslator(source="auto", target=targetlang).translate(text)
                break
            except Exception as e:
                logger.warning(e)
                continue
        logger.info(f"线程 {id+1} 翻译文本第 {i} 次:" + text)
    text = GoogleTranslator(source="auto", target=config["options"]["target_lang"]).translate(text)
    content_out[id] = text
    logger.info(f"线程 {id+1} 翻译完成")


'''text = "Hello"
file.seek(0)
lines = [line.rstrip('\n') for line in file.readlines()]
for i in range(len(lines)):
    print(f"第 {i + 1} 行文本: {lines[i]}")

results = []
open("out.txt", "w+", encoding=enc).close()
lll = 0
for content in lines:
    lll += 1
    text = content
    for i in tqdm(range(int(config["options"]["frequency"])), desc=f"正在翻译第 {lll} 行"):
        targetlang = shuffle_array(languages)[0]
        while True:
            try:
                text = GoogleTranslator(source="auto", target=targetlang).translate(text)
                break
            except Exception as e:
                print(e)
                continue

    text = GoogleTranslator(source="auto", target=config["options"]["target_lang"]).translate(text)
    print(f"{text}")
    results.append(text)
    open(config["options"]["file_out"], "a+", encoding=enc).write(text + "\n")
    time.sleep(1)
print("翻译已完成")
while 1:
    pass
    time.sleep(1)'''
file.seek(0)
content_scr = [line.rstrip('\n') for line in file.readlines()]
for i in range(len(content_scr)):
    logger.info(f"第 {i + 1} 行文本: {content_scr[i]}")

f = int(config["options"]["frequency"])
ln = len(content_scr)
threads = []
for i in range(ln):
    threads.append(threading.Thread(target=translator_, args=(f, content_scr[i], i)))
    threads[i].start()
    logger.info(f"已启动线程 {i}")
for i in range(ln):
    threads[i].join()
logger.info(content_out)
for i in range(ln):
    try:
        open(config["options"]["file_out"], "a+", encoding=enc).write(content_out[i] + "\n")
    except Exception as e:
        logger.error(e)
        logger.critical("文件写入出错,请检查配置文件!")
        raise SystemExit