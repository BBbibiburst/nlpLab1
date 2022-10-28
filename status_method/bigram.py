# coding=gbk
import json
import re
from math import log
import sys
import time

import TnT.TnT_OOV_discover
from config.post_process_config import Bigram_Rule_Dict
from post_process.post_process import post_process, get_rule_dict
from replace_dict import replace_dict
from config.status_config import *
import HMM.OOV_discover
import HMM.NAME_discover


def get_dict():
    with open(Bigram_Dict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def get_probability(word_dict, word1, word2):
    # print(word1,' ',word2)
    probability_bigram = 0
    if word_dict[word1].get(word2) is not None:
        probability_bigram = linear_interpolation * word_dict[word1][word2] / word_dict[word1]['__len__']
    probability_unigram = (1 - linear_interpolation) * word_dict[''][word2] / word_dict['']['__len__']
    probability = probability_bigram + probability_unigram
    return log(probability)


def replace_back(sentence_cut, replace_list):
    for key, item_list in replace_list.items():
        for item in item_list:
            sentence_cut = sentence_cut.replace(key, item, 1)
    return sentence_cut


def find_max_value_pos(dp, pos):
    max_value = -sys.maxsize
    max_pos = pos - 1
    for k, v in dp[pos].items():
        if v > max_value:
            max_value = v
            max_pos = k
    return max_pos


def add_dict(word_dict, last_word, word, p):
    if word_dict.get(last_word) is None:
        word_dict[last_word] = {}
    if word_dict[last_word].get(word) is None:
        word_dict[last_word][word] = 10 ** -p
        if word_dict[last_word].get('__len__') is None:
            word_dict[last_word]['__len__'] = 1


def add_into_dict(sentence_cut, word_dict, p):
    sentence_cut.append('__End__')
    last_word = ''
    for i in sentence_cut:
        word = i
        add_dict(word_dict, last_word, word, p)
        add_dict(word_dict, '', word, p)
        last_word = word


def bigram(sentence, word_dict, OOV_param=(11, 11)):
    sentence_past = sentence
    add_into_dict([i for i in sentence], word_dict, OOV_param[0])
    add_into_dict(TnT.TnT_OOV_discover.word_segment(sentence, TnT_dict), word_dict, OOV_param[1])
    add_into_dict(HMM.NAME_discover.word_segment(sentence, HMM_Name_dict), word_dict, OOV_param[1])
    # viterbi算法计算概率
    result = []
    sentence_length = len(sentence)
    dp = {d: {} for d in range(sentence_length + 1)}
    dp[0][0] = 0
    dp_back = {d: {} for d in range(sentence_length + 1)}
    minus_limit = -sys.maxsize >> 10
    for i in range(1, sentence_length + 1):
        for j in range(i):
            word2 = sentence[j:i]
            if word_dict[''].get(word2) is None:
                continue
            max_value = -sys.maxsize
            max_pos = 0
            for k, v in dp[j].items():
                word1 = sentence[k:j]
                if word_dict[''].get(word1) is None:
                    continue
                prob = get_probability(word_dict, word1, word2)
                value = v + prob
                if value > max_value:
                    max_value = value
                    max_pos = k
            if max_value > -sys.maxsize:
                dp[i][j] = max_value
                dp_back[i][j] = max_pos
    # 反向计算结果
    length = len(sentence)
    pos = find_max_value_pos(dp, length)
    last_pos = dp_back[length][pos]
    word = sentence[pos:]
    sentence = sentence[:pos]
    result.append(word)
    while sentence != '':
        length = len(sentence)
        pos = last_pos
        last_pos = dp_back[length][pos]
        word = sentence[pos:]
        sentence = sentence[:pos]
        result.insert(0, word)
    status_list = get_status_list(result)
    status_list = post_process(sentence_past, status_list, rule_dict)
    result = get_word_list_result(sentence_past, status_list)
    return result


def get_word_list_result(sentence, status_list):
    result = []
    while True:
        if len(sentence) == 0:
            break
        s = status_list.find('S')
        e = status_list.find('E')
        if s == -1:
            s = e
        if e == -1:
            e = s
        pos = min(s, e)
        result.append(sentence[:pos + 1])
        sentence = sentence[pos + 1:]
        status_list = status_list[pos + 1:]
    return result


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


def calculate(func, SolveFile, seg_gram, OOV_param=(14, 14)):
    print("正在获取词典...")
    print("词典获取完成")
    print("开始分词")
    times = 0
    start = time.time()
    with open(SolveFile, 'r', encoding='ansi') as solve_file:
        with open(seg_gram, 'w', encoding='ansi') as result_file:
            for sentence in solve_file:
                sentence = sentence.rstrip()
                if sentence == '':
                    result_file.write('\n')
                    continue
                    ##
                replace_list = {i: [] for i in replace_dict.values()}
                for key, value in replace_dict.items():
                    replace_list[value] = re.findall(key, sentence)
                    sentence = re.sub(key, value, sentence)
                    ##
                word_list = func(sentence, word_dictionary, OOV_param)
                sentence_cut = ''
                for word in word_list:
                    sentence_cut = sentence_cut + word + '/  '
                sentence_cut = replace_back(sentence_cut, replace_list)
                result_file.write(sentence_cut)
                result_file.write('\n')
                times += 1
                print("第{}个句子已完成分句".format(times))
    end = time.time()
    print('分词完成,用时{:.2f}s'.format((end - start)))


def solve(sentence, func, word_dictionary):
    if sentence == '':
        return ''
    replace_list = {i: [] for i in replace_dict.values()}
    for key, value in replace_dict.items():
        replace_list[value] = re.findall(key, sentence)
        sentence = re.sub(key, value, sentence)
        ##
    word_list = func(sentence, word_dictionary)
    sentence_cut = ''
    for word in word_list:
        sentence_cut = sentence_cut + word + '/  '
    sentence_cut = replace_back(sentence_cut, replace_list)
    return sentence_cut

word_dictionary = get_dict()
TnT_dict = TnT.TnT_OOV_discover.get_dict()
HMM_Name_dict = HMM.NAME_discover.get_dict()
rule_dict = get_rule_dict(Bigram_Rule_Dict)
if __name__ == '__main__':
    calculate(bigram, SolveFile, seg_Bigram)

