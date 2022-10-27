# coding=gbk
import json
import re
import sys
import time
from config.HMM_config import *
from replace_dict import replace_dict


def get_dict():
    with open(ProbDict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def viterbi(sentence, prob_dict):
    result = ''
    sentence_length = len(sentence)
    dp = {i: {} for i in range(sentence_length)}
    for i in range(sentence_length):
        for s in Status:
            sv = s.value
            if i == 0:
                emit = prob_dict['_C_'][sv].get(sentence[i])
                if emit is None:
                    emit = minus_limit
                dp[i][sv] = (prob_dict[''][sv] + emit, '')
            else:
                dp_p = -sys.maxsize
                dp_s = None
                for sv_pre in Status:
                    prob_pre = dp[i - 1][sv_pre.value][0]
                    trans = prob_dict[sv_pre.value][sv]
                    emit = prob_dict['_C_'][sv].get(sentence[i])
                    if emit == None:
                        emit = minus_limit
                    prob = prob_pre + trans + emit
                    if prob > dp_p:
                        dp_p = prob
                        dp_s = sv_pre.value
                dp[i][sv] = (dp_p, dp_s)

    dp_prob = -sys.maxsize
    dp_pos = None
    for s in Status:
        sv = s.value
        if sv in 'BM':
            continue
        if dp[sentence_length - 1][sv][0] > dp_prob:
            dp_prob = dp[sentence_length - 1][sv][0]
            dp_pos = sv
    result = dp_pos + result
    for i in range(sentence_length):
        result = dp[sentence_length - i - 1][result[0]][1] + result
    return result


def word_segment(sentence, prob_dict):
    result = []
    status_list = viterbi(sentence, prob_dict)
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


def replace_back(sentence_cut, replace_list):
    for key, item_list in replace_list.items():
        for item in item_list:
            sentence_cut = sentence_cut.replace(key, item, 1)
    return sentence_cut


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
                replace_list = {i: [] for i in replace_dict.values()}
                for key, value in replace_dict.items():
                    replace_list[value] = re.findall(key, sentence)
                    sentence = re.sub(key, value, sentence)
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
    # calculate(word_segment, SolveFile, seg_HMM)
    sentence = '19980101-01-003-006����ĳ�����������ʣ���������������������ƻ�Իͣ�����������͵�ϲ�����ա����ⳡ���й�������ί���������������칫���ȵ�λ�������Ϊ������Я�֡����໪�¡����������ֻ��ϣ��й����������������š������й��������š��Ϻ��������š��������������״������ݳ�������ָ�Ӽҳ����ҡ���������̷�����ֱ�ָ��������һ�������������������أ�������λ���ּ���ɵĴ����ֶ��Ա����ļ���;�տ�ļ���Ϊ���ڷ�����һ̨��ˮ׼�Ľ������ֻᡣ'
    print(solve(sentence, word_segment, get_dict()))
