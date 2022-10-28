# coding=gbk
import re

from replace_dict import replace_dict
from config.status_config import *
import json


def getWord(word):
    word_split = word.split(r'/')
    word = ''
    for i in range(len(word_split)):
        if i != len(word_split) - 1:
            word += word_split[i] + '/'
    word = word[:-1]
    return word


def get_word_list(line):
    word_list_result = []
    line_split = re.findall(r'\[[^\[\]]*\]\S*|[^\[\]\s]*/\S*', line)
    pos = 0
    for word in line_split:
        if word[0] == '[':
            word_split = re.findall(r'[^\[\s]*/[^/\s\]]*', word)
            word = ''
            for c in word_split:
                word += getWord(c)
        else:
            word = getWord(word)
        word_list_result.append(word)
    return word_list_result


def get_word_seperated_list(line):
    word_seperated_list_result = []
    line_split = re.findall(r'[^\[\s]*/[^/\s\]]*', line)
    for word in line_split:
        word = getWord(word)
        word_seperated_list_result.append(word)
    return word_seperated_list_result


def getBigram(word_list):
    word_list.insert(0, '')
    return [(word_list[i], word_list[i + 1]) for i in range(len(word_list) - 1)]


def get_complex_Bigram(line):
    result = []
    left_complex = re.findall(r'\[[^\[\]]*\]\S*\s\s[^/]*/\S*', line)
    right_complex = re.findall(r'[^/\s]*/\S*\s\s\[[^\[\]]*\]\S*', line)
    for word_partner in left_complex:
        left_list = re.findall(r'\[[^\[\]]*\]\S*', word_partner)[0]
        word_split = re.findall(r'[^\[\s]*/[^/\s\]]*', left_list)
        word = ''
        for c in word_split:
            word += getWord(c)
        right = re.findall(r'[^\[\s]*/[^/\s\]]*', word_partner)[-1]
        right = getWord(right)
        result.append((word, right))
    for word_partner in right_complex:
        right_list = re.findall(r'\[[^\[\]]*\]\S*', word_partner)[0]
        word_split = re.findall(r'[^\[\s]*/[^/\s\]]*', right_list)
        word = ''
        for c in word_split:
            word += getWord(c)
        left = re.findall(r'[^\[\s]*/[^/\s\]]*', word_partner)[0]
        left = getWord(left)
        result.append((left, word))
    return result


word_seg_dict = {}
print("正在形成词典...")


def make_dict(TrainingDataFile):
    global key
    with open(TrainingDataFile, 'r', encoding='ansi') as corpus:
        for line in corpus:
            line = line.rstrip()
            for key, value in replace_dict.items():
                line = re.sub(key, value, line)
            if include_complex_words:
                word_seperated_list = get_word_seperated_list(line)
                complex_list = get_complex_Bigram(line)
                word_bigram_seperated_list = getBigram(word_seperated_list)
                word_bigram_seperated_list.extend(complex_list)
            else:
                word_seperated_list = get_word_seperated_list(line)
                word_seperated_list.append('__End__')
                word_bigram_seperated_list = getBigram(word_seperated_list)
            for word_partner in word_bigram_seperated_list:
                if word_seg_dict.get(word_partner[0]) is None:
                    word_seg_dict[word_partner[0]] = {}
                if word_seg_dict[word_partner[0]].get(word_partner[1]) is None:
                    word_seg_dict[word_partner[0]][word_partner[1]] = 0
                if word_seg_dict[''].get(word_partner[1]) is None:
                    word_seg_dict[''][word_partner[1]] = 0
                word_seg_dict[word_partner[0]][word_partner[1]] += 1
                word_seg_dict[''][word_partner[1]] += 1


for data in TrainingDataFile:
    make_dict(data)


# 求解λ
lambda1 = lambda2 = 0
N = sum([word_seg_dict[''][s] for s in word_seg_dict[''].keys()])
for key1, sub_dict in word_seg_dict.items():
    for key2, value in sub_dict.items():
        f12 = word_seg_dict[key1][key2]
        f1 = word_seg_dict[''].get(key1)
        if f1 is None:
            f1 = 0
        f2 = word_seg_dict[''].get(key2)
        if f2 is None:
            f2 = 0
        num1 = 0
        num2 = 0
        if f1 - 1 != 0:
            num1 = (f12 - 1) / (f1 - 1)
        if N - 1 != 0:
            num2 = (f2 - 1) / (N - 1)
        max_value = max(num1, num2)
        if max_value == num1:
            lambda2 += f12
        else:
            lambda1 += f12
lambda_sum = lambda1 + lambda2
lambda1 /= lambda_sum
lambda2 /= lambda_sum
print('lambda1 = ', lambda1)
print('lambda2 = ', lambda2)
word_seg_dict['lambda1'] = lambda1
word_seg_dict['lambda2'] = lambda2


word_seg_dict['']['__total_len__'] = 0
word_seg_dict[''][''] = 0
for key in word_seg_dict.keys():
    if key in ['lambda1','lambda2']:
        continue
    word_seg_dict[key]['__len__'] = 0
    for val in word_seg_dict[key].values():
        word_seg_dict[key]['__len__'] += val
        word_seg_dict['']['__total_len__'] += val


with open(Bigram_Dict, 'w', encoding='ansi') as f:
    json_dump = json.dumps(word_seg_dict)
    f.write(json_dump)
print("词典已成型")
