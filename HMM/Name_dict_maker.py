# coding=gbk
import re
import sys

from HMM_config import *
import json
from math import log

from replace_dict import replace_dict


def getWord(word):
    word_split = word.split(r'/')
    word = ''
    word_class = word_split[-1]
    for i in range(len(word_split)):
        if i != len(word_split) - 1:
            word += word_split[i] + '/'
    word = word[:-1]
    return word, word_class


def get_word_seperated_list(line):
    word_seperated_list_result = []
    line_split = re.findall(r'[^\[\s]*/[^/\s\]]*', line)
    for word in line_split:
        word, word_class = getWord(word)
        word_seperated_list_result.append((word, word_class))
    return word_seperated_list_result


def default_probs_dict():
    return {'B': 0,
            'M': 0,
            'E': 0,
            'S': 0,
            'O': 0,}


def get_status_list(word_list):
    status_list = ''
    for word_pair in word_list:
        word = word_pair[0]
        word_class = word_pair[1]
        word_len = len(word)
        if word_class != 'nr':
            status_list += 'O' * word_len
            continue
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
            prob_dict[''][status_list[i]] += 1
        else:
            prob_dict[status_list[i - 1]][status_list[i]] += 1
        if prob_dict['_C_'][status_list[i]].get(sentence[i]) is None:
            prob_dict['_C_'][status_list[i]][sentence[i]] = 1
        prob_dict['_C_'][status_list[i]][sentence[i]] += 1


prob_dict = {}
print("正在形成HMM概率表...")
# 状态初始概率
prob_dict[''] = default_probs_dict()
# 状态转移
prob_dict['B'] = default_probs_dict()
prob_dict['M'] = default_probs_dict()
prob_dict['E'] = default_probs_dict()
prob_dict['S'] = default_probs_dict()
prob_dict['O'] = default_probs_dict()
prob_dict['_C_'] = {'B': {}, 'M': {}, 'E': {}, 'S': {}, 'O': {}}

def make_dict(TrainingDataFile):
    global key, value
    with open(TrainingDataFile, 'r', encoding='ansi') as corpus:
        for line in corpus:
            line = line.rstrip()
            for key, value in replace_dict.items():
                line = re.sub(key, value, line)
            word_list = get_word_seperated_list(line)
            status_list = get_status_list(word_list)
            word_list = [word_pair[0] for word_pair in word_list]
            add_word_into_dict(word_list, status_list, prob_dict)


def add_name():
    with open(NameTrainSet, 'r', encoding='ansi') as corpus:
        for line in corpus:
            word_list = get_word_seperated_list(line)
            line = re.sub(r'/nr  [\n]*', '', line)
            status_list = get_status_list(word_list)
            word_list = [word_pair[0] for word_pair in word_list]
            for i in range(len(line)):
                if prob_dict['_C_'][status_list[i]].get(line[i]) is None:
                    prob_dict['_C_'][status_list[i]][line[i]] = 0
                prob_dict['_C_'][status_list[i]][line[i]] += 1


for data in TrainingDataFile:
    make_dict(data)
add_name()

for key, value in prob_dict.items():
    total = 0
    if key == '_C_':
        continue
    for s, num in value.items():
        if s in 'BMESO':
            total += num
    for s in NameStatus:
        if prob_dict[key][s.value] == 0:
            prob_dict[key][s.value] = minus_limit
        else:
            prob_dict[key][s.value] = log((prob_dict[key][s.value]) / total)
for s in NameStatus:
    total = 0
    for key, value in prob_dict['_C_'][s.value].items():
        if key not in 'BMESO':
            total += value
    for key in prob_dict['_C_'][s.value].keys():
        if key not in 'BMESO':
            prob_dict['_C_'][s.value][key] = log((prob_dict['_C_'][s.value][key]) / total)

with open(NameProbDict, 'w', encoding='ansi') as f:
    json_dump = json.dumps(prob_dict)
    f.write(json_dump)
print("概率表已成型")
