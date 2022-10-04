# – coding: gbk –
import re
from phy_config import *

word_seg_dict = {}
print("正在形成词典...")
with open(TrainingDataFile, 'r', encoding='ansi') as corpus:
    for line in corpus:
        result = re.findall(r"[^\[\[\s]*/[^\[\]\s]*", line)
        for word_and_class in result:
            [word, word_class] = word_and_class.split('/')
            word_seg_dict[word] = word_class

with open(TrainingDataFile, 'r', encoding='ansi') as corpus:
    for line in corpus:
        result = re.findall(r"\[[^\[]*\][\S]*", line)
        for word_and_class in result:
            [word, word_class] = word_and_class.split(']')
            word = word + '  '
            word = re.sub(r"/\S*\s\s", '', word)
            word = word[1:]
            word_seg_dict[word] = word_class


with open(DictFile, 'w', encoding='ansi') as f:
    words = word_seg_dict.keys()
    words = sorted(words)
    for word in words:
        f.write(word)
        f.write('\n')
print("词典已成型")
