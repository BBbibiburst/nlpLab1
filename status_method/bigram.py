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
sentence = '１２月我在打游戏'
word_dict = get_dict()
answer = test(sentence, bigram, word_dict)
print(answer)
example = '19980101-03-001-004联合国会费比例的“能力支付”原则，即以各国国民生产总值占世界国民生产总值的比重作为基数，同时考虑人均国民生产总值和人均外债负担状况来计算各国应缴的会费额。美国是世界首富，但会费委员会为防止一国负担过重，规定了缴纳上限，美国会费分摊比例为２５％。可是，从１９９４年起，美国一直要求将其对联合国会费的分摊比例由２５％降到２０％，将维和费比例由３１％降至２５％，并以拒付会费作要挟。这种做法只能使联合国会费比例具有极大随意性，不利于联合国财政基础的稳定，遭到广大成员国的反对。在此情况下，美国仍继续拖欠会费１３亿多美元，并且提出联合国改革尺度法案，把付清欠款同联合国改革挂钩，结果遭到空前孤立。'
answer = test(example, bigram, word_dict)
print(answer)
