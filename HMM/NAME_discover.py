# coding=gbk
import json
import re
import sys
import time
from HMM.HMM_config import *
from replace_dict import replace_dict

def get_dict():
    with open(NameProbDict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict

def viterbi(sentence, prob_dict):
    result = ''
    sentence_length = len(sentence)
    dp = {i: {} for i in range(sentence_length)}
    for i in range(sentence_length):
        for s in NameStatus:
            sv = s.value
            if i == 0:
                emit = prob_dict['_C_'][sv].get(sentence[i])
                if emit == None:
                    emit = minus_limit
                dp[i][sv] = (prob_dict[''][sv] + emit, '')
            else:
                dp_p = -sys.maxsize
                dp_s = None
                for sv_pre in NameStatus:
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
    for s in NameStatus:
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
        o = status_list.find('O')
        if s == -1:
            s = sys.maxsize
        if e == -1:
            e = sys.maxsize
        if o == -1:
            o = sys.maxsize
        pos = min(s, e, o)
        if pos != o:
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
                replace_list = {i: [] for i in replace_dict.values()}
                for key, value in replace_dict.items():
                    replace_list[value] = re.findall(key, sentence)
                    sentence = re.sub(key, value, sentence)
                word_list = func(sentence, word_dictionary)
                sentence_cut = ''
                for word in word_list:
                    sentence_cut = sentence_cut + word + '/  '
                #sentence_cut = replace_back(sentence_cut, replace_list)
                result_file.write(sentence_cut)
                result_file.write('\n')
                times += 1
                print("第{}个句子已完成分句".format(times))
    end = time.time()
    print('分词完成,用时{:.2f}s'.format((end - start)))


if __name__ == '__main__':
    calculate(word_segment, SolveFile, seg_Name)
