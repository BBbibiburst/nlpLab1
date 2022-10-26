# coding=gbk
import json
import re
from math import log
import sys
import time
from replace_dict import replace_dict
from CBGM.CBGM_config import *


def get_dict():
    with open(ProbDict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def get_probability(word_dict, word1, word2):
    # print(word1,' ',word2)
    probability_bigram = minus_limit
    if word_dict[word1].get(word2) is not None:
        probability_bigram = word_dict['lambda2'] * word_dict[word1][word2]
    probability_unigram = 0.00001 * word_dict['lambda1'] * word_dict['BACK_OFF'][word2]
    probability = probability_bigram + probability_unigram
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
        if dp[pos][s.value] > max_value:
            max_value = dp[pos][s.value]
            max_pos = s.value
    return max_value, max_pos


def cbgm_viterbi(sentence, word_dictionary):
    result = ''
    dp = {i: {s.value: -sys.maxsize for s in Status} for i in range(len(sentence))}
    dp_back = {i: {s.value: None for s in Status} for i in range(len(sentence))}
    for i in range(len(sentence)):
        for s in Status:
            sv = s.value
            if word_dictionary['BACK_OFF'].get(sentence[i] + ' ' + sv) is None:
                if i == 0:
                    dp[i][sv] = minus_limit
                    dp_back[i][sv] = ''
                else:
                    max_value, max_pos = find_max_pos(dp, i - 1)
                    dp[i][sv] = minus_limit + max_value
                    dp_back[i][sv] = max_pos
                continue
            if i == 0:
                if sv in 'EM':
                    continue
                dp[i][sv] = get_probability(word_dictionary, ' ', sentence[i] + ' ' + sv)
                dp_back[i][sv] = ''
            else:
                dp_isv = -sys.maxsize
                for s_pre in Status:
                    sv_pre = s_pre.value
                    if sv in 'BS' and sv_pre in 'BM':
                        continue
                    if sv in 'ME' and sv_pre in 'ES':
                        continue
                    if word_dictionary['BACK_OFF'].get(sentence[i - 1] + ' ' + sv_pre) is None:
                        continue
                    if dp[i - 1].get(sv_pre) is None:
                        continue
                    dp_value = get_probability(word_dictionary, sentence[i - 1] + ' ' + sv_pre,
                                               sentence[i] + ' ' + sv) + dp[i - 1][sv_pre]
                    if dp_value > dp_isv:
                        dp_isv = dp_value
                        dp_back[i][sv] = sv_pre
                if dp_isv != -sys.maxsize:
                    dp[i][sv] = dp_isv
                else:
                    max_value, max_pos = find_max_pos(dp, i - 1)
                    dp[i][sv] = minus_limit + max_value
                    dp_back[i][sv] = max_pos

    max_value = -sys.maxsize
    max_pos = 'S'
    for sv in dp[len(sentence) - 1].keys():
        if sv in 'BM':
            continue
        if dp[len(sentence) - 1][sv] > max_value:
            max_value = dp[len(sentence) - 1][sv]
            max_pos = sv
    length = len(sentence)
    for i in range(length):
        result = max_pos + result
        max_pos = dp_back[length - 1 - i][max_pos]
    return result


def cbgm(sentence, prob_dict):
    result = []
    status_list = cbgm_viterbi(sentence, prob_dict)
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
    print("���ڻ�ȡ�ʵ�...")
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


if __name__ == '__main__':
    word_dictionary = get_dict()
    calculate(cbgm, SolveFile, seg_CBGM)
    sentence = '19980101-01-003-006����ĳ�����������ʣ���������������������ƻ�Իͣ�����������͵�ϲ�����ա����ⳡ���й�������ί���������������칫���ȵ�λ�������Ϊ������Я�֡����໪�¡����������ֻ��ϣ��й����������������š������й��������š��Ϻ��������š��������������״������ݳ�������ָ�Ӽҳ����ҡ���������̷�����ֱ�ָ��������һ�������������������أ�������λ���ּ���ɵĴ����ֶ��Ա����ļ���;�տ�ļ���Ϊ���ڷ�����һ̨��ˮ׼�Ľ������ֻᡣ'
    print(solve(sentence, cbgm, word_dictionary))
