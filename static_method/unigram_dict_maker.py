# – coding: gbk –
import re
from static_config import *
import json

word_seg_dict = {}
print("正在形成词典...")
with open(TrainingDataFile, 'r', encoding='ansi') as corpus:
    for line in corpus:
        result = re.findall(r"[^\[\[\s]*/[^\[\]\s]*", line)
        for word_and_class in result:
            [word, word_class] = word_and_class.split('/')
            if word_seg_dict.get(word) is not None:
                word_seg_dict[word] += 1
            else:
                word_seg_dict[word] = 1

with open(TrainingDataFile, 'r', encoding='ansi') as corpus:
    for line in corpus:
        result = re.findall(r"\[[^\[]*\][\S]*", line)
        for word_and_class in result:
            [word, word_class] = word_and_class.split(']')
            word = word + '  '
            word = re.sub(r"/\S*\s\s", '', word)
            word = word[1:]
            if word_seg_dict.get(word) is not None:
                word_seg_dict[word] += 1
            else:
                word_seg_dict[word] = 1

with open(Unigram_Dict, 'w', encoding='ansi') as f:
    json_dump = json.dumps(word_seg_dict)
    f.write(json_dump)
print("词典已成型")
