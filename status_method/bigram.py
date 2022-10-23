# coding=gbk
import json
import re
from math import log
import sys
import time

from replace_dict import replace_dict
from status_config import *


def get_dict():
    with open(Bigram_Dict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def get_probability(word_dict, word1, word2):
    if word_dict.get(word1) is None:
        return 0
    if word_dict[word1].get(word2) is None:
        return -1000 / (len(word2) + 1)
    else:
        probability = word_dict[word1][word2] + 1
        return log(probability)


def replace_back(sentence_cut, replace_list):
    for key, item_list in replace_list.items():
        for item in item_list:
            sentence_cut = sentence_cut.replace(key, item, 1)
    return sentence_cut


def bigram(sentence, word_dict):
    result = []
    sentence_length = len(sentence)
    dp = {d: {} for d in range(sentence_length + 1)}
    dp[0][0] = 0
    minus_limit = -sys.maxsize >> 10
    for i in range(1, sentence_length + 1):
        #dp[i][i - 1] = (minus_limit >> 10, -1)
        for j in range(i):
            word2 = sentence[j:i]
            if word_dict[''].get(word2) is None:
                continue
            max_value = minus_limit
            for k, v in dp[j].items():
                word1 = sentence[k:j]
                if word_dict[''].get(word1) is None:
                    continue
                prob = get_probability(word_dict, word1, word2)
                value = v + prob
                if value > max_value:
                    max_value = value
            if max_value > minus_limit:
                dp[i][j] = max_value

    while True:
        if sentence == '':
            break
        length = len(sentence)
        max_pos = 0
        max_value = -sys.maxsize
        for i, v in dp[length].items():
            if v > max_value:
                max_value = v
                max_pos = i
        result.insert(0, sentence[max_pos:])
        sentence = sentence[:max_pos]
    return result


def calculate(func, SolveFile, seg_gram):
    print("正在获取词典...")
    word_dictionary = get_dict()
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
                word_list = func(sentence, word_dictionary)
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


def test(sentence, func, word_dictionary):
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


# calculate(bigram, SolveFile, seg_Bigram)
sentence = '19980101-01-001-004１２月３１日，中共中央总书记、国家主席江泽民发表１９９８年新年讲话《迈向充满希望的新世纪》。（新华社记者兰红光摄）'
word_dict = get_dict()
answer = test(sentence, bigram, word_dict)
print(answer)
