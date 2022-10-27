# coding=gbk
import re

from config.CBGM_config import *
import json
from math import log

from replace_dict import replace_dict


def getWord(word):
    word_split = word.split(r'/')
    word = ''
    for i in range(len(word_split)):
        if i != len(word_split) - 1:
            word += word_split[i] + '/'
    word = word[:-1]
    return word


def get_word_seperated_list(line):
    word_seperated_list_result = []
    line_split = re.findall(r'[^\[\s]*/[^/\s\]]*', line)
    for word in line_split:
        word = getWord(word)
        word_seperated_list_result.append(word)
    return word_seperated_list_result


def get_status_list(word_list):
    status_list = ''
    for word in word_list:
        word_len = len(word)
        if word_len == 1:
            status_list += 'S'
        else:
            for i in range(word_len):
                if i == 0:
                    status_list += 'B'
                elif i == word_len - 1:
                    status_list += 'E'
                else:
                    status_list += 'M'
    return status_list


def make_word_status_pair_list(word_list, status_list):
    sentence = ''
    for word in word_list:
        sentence += word
    return [sentence[i]+' '+status_list[i] for i in range(len(sentence))]


def add_word_into_dict(word_list, status_list, prob_dict):
    wsp_list = make_word_status_pair_list(word_list, status_list)
    wsp_list.append('END S')
    last_wsp = ' '
    for ws_pair in wsp_list:
        if prob_dict.get(last_wsp) is None:
            prob_dict[last_wsp] = {}
        if prob_dict[last_wsp].get(ws_pair) is None:
            prob_dict[last_wsp][ws_pair] = 0
        prob_dict[last_wsp][ws_pair] += 1
        if prob_dict.get('BACK_OFF') is None:
            prob_dict['BACK_OFF'] = {}
        if prob_dict['BACK_OFF'].get(ws_pair) is None:
            prob_dict['BACK_OFF'][ws_pair] = 0
        prob_dict['BACK_OFF'][ws_pair] += 1
        last_wsp = ws_pair


def make_dict(TrainingDataFile):
    with open(TrainingDataFile, 'r', encoding='ansi') as corpus:
        for line in corpus:
            line = line.rstrip()
            for key, value in replace_dict.items():
                line = re.sub(key, value, line)
            word_list = get_word_seperated_list(line)
            status_list = get_status_list(word_list)
            add_word_into_dict(word_list, status_list, prob_dict)


prob_dict = {}
print("正在形成词典...")
for data in TrainingDataFile:
    make_dict(data)


# 求解λ
lambda1 = lambda2 = 0
N = sum([prob_dict['BACK_OFF'][s] for s in prob_dict['BACK_OFF'].keys()])
for key1, sub_dict in prob_dict.items():
    for key2, value in sub_dict.items():
        f12 = prob_dict[key1][key2]
        f1 = prob_dict['BACK_OFF'].get(key1)
        if f1 is None:
            f1 = 0
        f2 = prob_dict['BACK_OFF'].get(key2)
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
prob_dict['lambda1'] = lambda1
prob_dict['lambda2'] = lambda2


for key1, sub_dict in prob_dict.items():
    if key1 in ['lambda1','lambda2']:
        continue
    total = 0
    for key2, value in sub_dict.items():
        total += value
    for key2 in sub_dict.keys():
        prob_dict[key1][key2] = log((prob_dict[key1][key2]) / total)

with open(ProbDict, 'w', encoding='ansi') as f:
    json_dump = json.dumps(prob_dict)
    f.write(json_dump)
print("词典已成型")
