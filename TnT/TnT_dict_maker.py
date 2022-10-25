# coding=gbk
import re
import sys

from TnT_config import *
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


def default_probs_dict():
    return {'B': 0, 'M': 0, 'E': 0, 'S': 0, '': 0, 'BACK_OFF': 0}


def default_TnT_probs_dict():
    TnT_dict = default_probs_dict()
    for TnT_key in TnT_dict.keys():
        TnT_dict[TnT_key] = default_probs_dict()
    return TnT_dict


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


def add_word_into_dict(word_list, status_list, prob_dict):
    sentence = ''
    for word in word_list:
        sentence += word
    length = len(sentence)
    for i in range(length):
        if i == 0:
            prob_dict[''][''][status_list[i]] += 1
            prob_dict['BACK_OFF'][''][status_list[i]] += 1
        elif i == 1:
            prob_dict[''][status_list[i - 1]][status_list[i]] += 1
            prob_dict['BACK_OFF'][status_list[i - 1]][status_list[i]] += 1
        else:
            prob_dict[status_list[i - 2]][status_list[i - 1]][status_list[i]] += 1
            prob_dict['BACK_OFF'][status_list[i - 1]][status_list[i]] += 1
        prob_dict['BACK_OFF']['BACK_OFF'][status_list[i]] += 1
        if prob_dict[status_list[i]].get(sentence[i]) is None:
            prob_dict[status_list[i]][sentence[i]] = 0
        prob_dict[status_list[i]][sentence[i]] += 1


prob_dict = {}
print("正在形成HMM概率表...")
# 状态初始概率
prob_dict[''] = default_TnT_probs_dict()
# 回退概率
prob_dict['BACK_OFF'] = default_TnT_probs_dict()
# 状态转移
prob_dict['B'] = default_TnT_probs_dict()
prob_dict['M'] = default_TnT_probs_dict()
prob_dict['E'] = default_TnT_probs_dict()
prob_dict['S'] = default_TnT_probs_dict()


def make_dict(TrainingDataFile):
    global key, value
    with open(TrainingDataFile, 'r', encoding='ansi') as corpus:
        for line in corpus:
            line = line.rstrip()
            for key, value in replace_dict.items():
                line = re.sub(key, value, line)
            word_list = get_word_seperated_list(line)
            status_list = get_status_list(word_list)
            add_word_into_dict(word_list, status_list, prob_dict)


for data in TrainingDataFile:
    make_dict(data)

# 求解λ
lambda1 = lambda2 = lambda3 = 0
for s1 in Status:
    for s2 in Status:
        for s3 in Status:
            sv1 = s1.value
            sv2 = s2.value
            sv3 = s3.value
            f123 = prob_dict[sv1][sv2][sv3]
            f12 = prob_dict['BACK_OFF'][sv1][sv2]
            f23 = prob_dict['BACK_OFF'][sv2][sv3]
            f2 = prob_dict['BACK_OFF']['BACK_OFF'][sv2]
            f3 = prob_dict['BACK_OFF']['BACK_OFF'][sv3]
            num1 = 0
            num2 = 0
            num3 = 0
            N = sum([prob_dict['BACK_OFF']['BACK_OFF'][s.value] for s in Status])
            if f12 != 0:
                num1 = (f123 - 1) / (f12 - 1)
            if f2 != 0:
                num2 = (f23 - 1) / (f2 - 1)
            if N != 0:
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
# tri-gram概率
for key1, sub_dict in prob_dict.items():
    if key1 not in "BMES":
        continue
    for key2, value in sub_dict.items():
        if key2 not in "BMES":
            continue
        total = 0
        for s, num in value.items():
            if s in 'BMES':
                total += num
        for s in Status:
            if prob_dict[key1][key2][s.value] == 0:
                prob_dict[key1][key2][s.value] = minus_limit
            else:
                prob_dict[key1][key2][s.value] = log((prob_dict[key1][key2][s.value]) / total)
for s in Status:
    total = 0
    for key, value in prob_dict[s.value].items():
        if key not in 'BMES' and key != 'BACK_OFF':
            total += value
    for key in prob_dict[s.value].keys():
        if key not in 'BMES' and key != 'BACK_OFF':
            prob_dict[s.value][key] = log((prob_dict[s.value][key]) / total)

# bigram概率
for key, value in prob_dict['BACK_OFF'].items():
    total = 0
    for s, num in value.items():
        if s in 'BMES':
            total += num
    for s in Status:
        if prob_dict['BACK_OFF'][key][s.value] == 0:
            prob_dict['BACK_OFF'][key][s.value] = minus_limit
        else:
            prob_dict['BACK_OFF'][key][s.value] = log((prob_dict['BACK_OFF'][key][s.value]) / total)

# unigram概率
total = 0
for key, value in prob_dict['BACK_OFF']['BACK_OFF'].items():
    total += value
for s in Status:
    if prob_dict['BACK_OFF']['BACK_OFF'][s.value] == 0:
        prob_dict['BACK_OFF']['BACK_OFF'][s.value] = minus_limit
    else:
        prob_dict['BACK_OFF']['BACK_OFF'][s.value] = log((prob_dict['BACK_OFF']['BACK_OFF'][s.value]) / total)

with open(ProbDict, 'w', encoding='ansi') as f:
    json_dump = json.dumps(prob_dict)
    f.write(json_dump)
print("概率表已成型")
