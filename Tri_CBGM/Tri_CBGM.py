# coding=gbk
import json
import re
from math import log
import sys
import time

from config.post_process_config import Tri_CBGM_Rule_Dict
from post_process.post_process import post_process, get_rule_dict
from replace_dict import replace_dict
from config.Tri_CBGM_config import *


def get_dict():
    with open(ProbDict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def get_probability(word_dict, word1, word2, word3):
    # print(word1,' ',word2)
    probability_trigram = minus_limit
    probability_bigram = minus_limit
    probability_unigram = minus_limit
    if word_dict.get(word1) is not None and word_dict[word1].get(word2) is not None and word_dict[word1][word2].get(
            word3) is not None:
        probability_trigram = word_dict['lambda3'] * word_dict[word1][word2][word3]
    if word_dict['BACK_OFF'].get(word2) is not None and word_dict['BACK_OFF'][word2].get(word3) is not None:
        probability_bigram = word_dict['lambda2'] * word_dict['BACK_OFF'][word2][word3]
    if word_dict['BACK_OFF']['BACK_OFF'].get(word3) is not None:
        probability_unigram = word_dict['lambda1'] * word_dict['BACK_OFF']['BACK_OFF'][word3]
    probability = probability_trigram + probability_bigram + probability_unigram
    return probability


def replace_back(sentence_cut, replace_list):
    for key, item_list in replace_list.items():
        for item in item_list:
            sentence_cut = sentence_cut.replace(key, item, 1)
    return sentence_cut


def find_max_pos(dp, pos):
    max_value = -sys.maxsize
    max_pos = None
    for s in Status:
        for s2 in Status:
            if dp[pos][s.value][s2.value] > max_value:
                max_value = dp[pos][s.value][s2.value]
                max_pos = (s.value, s2.value)
    return max_value, max_pos


def find_max_pos_1(dp, pos):
    max_value = -sys.maxsize
    max_pos = None
    for s in Status:
        if dp[pos][''][s.value] > max_value:
            max_value = dp[pos][''][s.value]
            max_pos = ('', s.value)
    return max_value, max_pos


def find_max_pos_2(dp, pos):
    max_value = -sys.maxsize
    max_pos = None
    for s in Status:
        for s2 in Status:
            if s2.value in 'BM':
                continue
            if dp[pos][s.value][s2.value] > max_value:
                max_value = dp[pos][s.value][s2.value]
                max_pos = (s.value, s2.value)
    return max_value, max_pos


def tri_cbgm_viterbi(sentence, word_dictionary):
    if len(sentence) == 1:
        return 'S'
    result = ''
    dp = {i: {s.value: {s2.value: -sys.maxsize >> 10 for s2 in Status} for s in Status} for i in range(len(sentence))}
    dp_back = {i: {s.value: {s2.value: None for s2 in Status} for s in Status} for i in range(len(sentence))}
    dp[0] = {'': {}}
    dp_back[0] = {'': {}}
    for i in range(len(sentence)):
        for s in Status:
            sv = s.value
            if i == 0:
                if sv in 'EM':
                    continue
                dp[i][''][sv] = get_probability(word_dictionary, ' ', ' ', sentence[i] + ' ' + sv)
                dp_back[i][''][sv] = ('', '')
                continue
            for s_pre in Status:
                sv_pre = s_pre.value
                if i == 1:
                    if dp[i - 1][''].get(sv_pre) is None:
                        continue
                    dp[i][sv_pre][sv] = get_probability(word_dictionary, ' ', sentence[i - 1] + ' ' + sv_pre,
                                                        sentence[i] + ' ' + sv) + dp[i - 1][''][sv_pre]
                    dp_back[i][sv_pre][sv] = ('', sv_pre)
                else:
                    dp_isv = -sys.maxsize
                    if sv in 'BS' and sv_pre in 'BM':
                        continue
                    if sv in 'ME' and sv_pre in 'ES':
                        continue
                    for s_pre2 in Status:
                        sv_pre2 = s_pre2.value
                        if sv_pre in 'BS' and sv_pre2 in 'BM':
                            continue
                        if sv_pre in 'ME' and sv_pre2 in 'ES':
                            continue
                        if dp[i - 1].get(sv_pre) is None:
                            continue
                        dp_value = get_probability(word_dictionary, sentence[i - 2] + ' ' + sv_pre2,
                                                   sentence[i - 1] + ' ' + sv_pre,
                                                   sentence[i] + ' ' + sv) + dp[i - 1][sv_pre2][sv_pre]
                        if dp_value > dp_isv:
                            dp_isv = dp_value
                            dp_back[i][sv_pre][sv] = (sv_pre2, sv_pre)
                    if dp_isv != -sys.maxsize:
                        dp[i][sv_pre][sv] = dp_isv
                    else:
                        max_value, max_pos = find_max_pos(dp, i - 1)
                        dp[i][sv_pre][sv] = minus_limit + max_value
                        dp_back[i][sv_pre][sv] = max_pos

    length = len(sentence)
    max_value, max_pos = find_max_pos_2(dp, length - 1)
    result = max_pos[0] + max_pos[1] + result
    for i in range(length):
        max_pos = dp_back[length - 1 - i][max_pos[0]][max_pos[1]]
        result = max_pos[0] + result
    return result


def tri_cbgm(sentence, prob_dict):
    result = []
    status_list = tri_cbgm_viterbi(sentence, prob_dict)
    status_list = post_process(sentence, status_list, TC_rule_dict)
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


def calculate(func, SolveFile, seg_gram):
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


TC_rule_dict = get_rule_dict(Tri_CBGM_Rule_Dict)
if __name__ == '__main__':
    word_dictionary = get_dict()
    calculate(tri_cbgm, SolveFile, seg_CBGM)
