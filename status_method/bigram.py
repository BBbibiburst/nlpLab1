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
    if word_dict.get(word1) is None or word_dict[word1].get(word2) is None:
        return (1 - linear_interpolation) * word_dict[''][word2]
    else:
        probability = linear_interpolation * word_dict[word1][word2] + (1 - linear_interpolation) * word_dict[''][word2]
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


def bigram(sentence, word_dict):
    # viterbi�㷨�������
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
                prob = get_probability(word_dict, word1, word2)
                value = v + prob
                if value > max_value:
                    max_value = value
                    max_pos = k
            if max_value > -sys.maxsize:
                dp[i][j] = max_value
                dp_back[i][j] = max_pos
        if len(dp[i]) == 0:
            dp[i][i - 1] = minus_limit
            if i - 2 > 0:
                dp_back[i][i - 1] = i - 2
            else:
                dp_back[i][i - 1] = 0
    # ���������
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

    return result


def calculate(func, SolveFile, seg_gram):
    print("���ڻ�ȡ�ʵ�...")
    word_dictionary = get_dict()
    print("�ʵ��ȡ���")
    print("��ʼ�ִ�")
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
                print("��{}����������ɷ־�".format(times))
    end = time.time()
    print('�ִ����,��ʱ{:.2f}s'.format((end - start)))


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
sentence = '���������ڴ���Ϸ'
word_dict = get_dict()
answer = test(sentence, bigram, word_dict)
print(answer)
example = '19980101-03-001-004���Ϲ���ѱ����ġ�����֧����ԭ�򣬼��Ը�������������ֵռ�������������ֵ�ı�����Ϊ������ͬʱ�����˾�����������ֵ���˾���ծ����״�����������Ӧ�ɵĻ�Ѷ�����������׸��������ίԱ��Ϊ��ֹһ���������أ��涨�˽������ޣ�������ѷ�̯����Ϊ�����������ǣ��ӣ���������������һֱҪ��������Ϲ���ѵķ�̯�����ɣ�������������������ά�ͷѱ����ɣ��������������������Ծܸ������ҪЮ����������ֻ��ʹ���Ϲ���ѱ������м��������ԣ����������Ϲ������������ȶ����⵽����Ա���ķ��ԡ��ڴ�����£������Լ�����Ƿ��ѣ����ڶ���Ԫ������������Ϲ��ĸ�߶ȷ������Ѹ���Ƿ��ͬ���Ϲ��ĸ�ҹ�������⵽��ǰ������'
answer = test(example, bigram, word_dict)
print(answer)
