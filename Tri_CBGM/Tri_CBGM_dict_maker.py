# coding=gbk
import re

from config.Tri_CBGM_config import *
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
    return [sentence[i] + ' ' + status_list[i] for i in range(len(sentence))]


def add_word_into_dict(word_list, status_list, prob_dict):
    wsp_list = make_word_status_pair_list(word_list, status_list)
    wsp_list.append('END1 S')
    wsp_list.append('END2 S')
    last_wsp = ' '
    last_wsp2 = ' '
    for ws_pair in wsp_list:
        # trigram
        if prob_dict.get(last_wsp2) is None:
            prob_dict[last_wsp2] = {}
        if prob_dict[last_wsp2].get(last_wsp) is None:
            prob_dict[last_wsp2][last_wsp] = {}
        if prob_dict[last_wsp2][last_wsp].get(ws_pair) is None:
            prob_dict[last_wsp2][last_wsp][ws_pair] = 0
        prob_dict[last_wsp2][last_wsp][ws_pair] += 1
        # bigram
        if prob_dict.get('BACK_OFF') is None:
            prob_dict['BACK_OFF'] = {}
        if prob_dict['BACK_OFF'].get(last_wsp) is None:
            prob_dict['BACK_OFF'][last_wsp] = {}
        if prob_dict['BACK_OFF'][last_wsp].get(ws_pair) is None:
            prob_dict['BACK_OFF'][last_wsp][ws_pair] = 0
        prob_dict['BACK_OFF'][last_wsp][ws_pair] += 1
        # unigram
        if prob_dict['BACK_OFF'].get('BACK_OFF') is None:
            prob_dict['BACK_OFF']['BACK_OFF'] = {}
        if prob_dict['BACK_OFF']['BACK_OFF'].get(ws_pair) is None:
            prob_dict['BACK_OFF']['BACK_OFF'][ws_pair] = 0
        prob_dict['BACK_OFF']['BACK_OFF'][ws_pair] += 1
        last_wsp2 = last_wsp
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


def get_f(k1, k2, k3):
    if prob_dict.get(k1) is None:
        return 0
    if prob_dict[k1].get(k2) is None:
        return 0
    p = prob_dict[k1][k2].get(k3)
    if p is None:
        return 0
    else:
        return p


# 求解λ
lambda1 = lambda2 = lambda3 = 0
N = sum([prob_dict['BACK_OFF']['BACK_OFF'][key] for key in prob_dict['BACK_OFF']['BACK_OFF'].keys()])
for key1, sub_dict1 in prob_dict.items():
    if key1 == 'BACK_OFF':
        continue
    for key2, sub_dict2 in sub_dict1.items():
        if key2 == 'BACK_OFF':
            continue
        for key3, sub_dict3 in sub_dict2.items():
            f123 = get_f(key1, key2, key3)
            f12 = get_f('BACK_OFF', key1, key2)
            f23 = get_f('BACK_OFF', key2, key3)
            f2 = get_f('BACK_OFF', 'BACK_OFF', key2)
            f3 = get_f('BACK_OFF', 'BACK_OFF', key3)
            num1 = 0
            num2 = 0
            num3 = 0
            if f12 - 1 != 0:
                num1 = (f123 - 1) / (f12 - 1)
            if f2 - 1 != 0:
                num2 = (f23 - 1) / (f2 - 1)
            if N - 1 != 0:
                num3 = (f3 - 1) / (N - 1)
            max_value = max(num1, num2, num3)
            if max_value == num1:
                lambda3 += f123
            elif max_value == num2:
                lambda2 += f123
            else:
                lambda1 += f123
lambda_sum = lambda1 + lambda2 + lambda3
lambda1 /= lambda_sum
lambda2 /= lambda_sum
lambda3 /= lambda_sum
print('lambda1 = ', lambda1)
print('lambda2 = ', lambda2)
print('lambda3 = ', lambda3)
prob_dict['lambda1'] = lambda1
prob_dict['lambda2'] = lambda2
prob_dict['lambda3'] = lambda3

for key1, sub_dict1 in prob_dict.items():
    if key1 in ['lambda1', 'lambda2', 'lambda3']:
        continue
    for key2, sub_dict2 in sub_dict1.items():
        total = 0
        for key3, value in sub_dict2.items():
            total += value
        for key3 in sub_dict2.keys():
            prob_dict[key1][key2][key3] = log((prob_dict[key1][key2][key3]) / total)

with open(ProbDict, 'w', encoding='ansi') as f:
    json_dump = json.dumps(prob_dict)
    f.write(json_dump)
print("词典已成型")
