# coding=gbk
import json
import re
import sys
import time
from config.TnT_config import *
from replace_dict import replace_dict


def get_dict():
    with open(NameProbDict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def get_prob(prob_dict, tag1, tag2, tag3):
    # return prob_dict[tag1][tag2][tag3]
    return prob_dict['lambda1'] * prob_dict['BACK_OFF']['BACK_OFF'][tag3] \
        + prob_dict['lambda2'] * prob_dict['BACK_OFF'][tag2][tag3] \
        + prob_dict['lambda3'] * prob_dict[tag1][tag2][tag3]


def viterbi(sentence, prob_dict):
    result = ''
    sentence_length = len(sentence)
    dp = {i: {'B': {}, 'M': {}, 'E': {}, 'S': {}, 'O': {}} for i in range(sentence_length)}
    dp[0][''] = {}
    for i in range(sentence_length):
        for s in NameStatus:
            sv = s.value
            if i == 0:
                if sv in 'EM':
                    continue
                emit = prob_dict['_C_'][sv].get(sentence[i])
                if emit is None:
                    emit = minus_limit
                dp[i][''][sv] = (get_prob(prob_dict, '', '', sv) + emit, '', '')
            elif i == 1:
                emit = prob_dict['_C_'][sv].get(sentence[i])
                if emit is None:
                    emit = minus_limit
                for sv_pre in NameStatus:
                    if sv_pre.value in 'BMO' and sv in 'BS':
                        continue
                    if sv_pre.value == 'ESO' and sv == 'M':
                        continue
                    if dp[i-1][''].get(sv_pre.value) is None:
                        continue
                    dp[i][sv_pre.value][sv] = (get_prob(prob_dict, '', sv_pre.value, sv) + emit, '', sv_pre.value)
            else:
                for sv_pre in NameStatus:
                    if sv_pre.value in 'BMO' and sv in 'BS':
                        continue
                    if sv_pre.value == 'ESO' and sv == 'M':
                        continue
                    dp_p = -sys.maxsize
                    dp_s = None
                    dp_s2 = None
                    for sv_pre2 in NameStatus:
                        value = dp[i - 1][sv_pre2.value].get(sv_pre.value)
                        if value is None:
                            continue
                        prob_pre = value[0]
                        trans = get_prob(prob_dict, sv_pre2.value, sv_pre.value, sv)
                        emit = prob_dict['_C_'][sv].get(sentence[i])
                        if emit is None:
                            emit = minus_limit
                        prob = prob_pre + trans + emit
                        if prob > dp_p:
                            dp_p = prob
                            dp_s = sv_pre.value
                            dp_s2 = sv_pre2.value
                    if dp[i-1][dp_s2].get(dp_s) is None:
                        continue
                    dp[i][sv_pre.value][sv] = (dp_p, dp_s2, dp_s)

    dp_prob = -sys.maxsize
    dp_pos = None
    for s in NameStatus:
        sv = s.value
        if sv in 'BM':
            continue
        for sv_pre in NameStatus:
            dp_value = dp[sentence_length - 1][sv_pre.value].get(sv)
            if dp_value is None:
                continue
            if dp_value[0] > dp_prob:
                dp_prob = dp_value[0]
                dp_pos = (sv_pre.value, sv)
        if sentence_length == 1:
            dp_value = dp[sentence_length - 1][''].get(sv)
            if dp_value is None:
                continue
            if dp_value[0] > dp_prob:
                dp_prob = dp_value[0]
                dp_pos = ('', sv)
    result = dp_pos[0] + dp_pos[1] + result
    for i in range(sentence_length):
        dp_pos = dp[sentence_length - i - 1][dp_pos[0]][dp_pos[1]][1:3]
        result = dp_pos[0] + result
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
                sentence_cut = replace_back(sentence_cut, replace_list)
                result_file.write(sentence_cut)
                result_file.write('\n')
                times += 1
                print("第{}个句子已完成分句".format(times))
    end = time.time()
    print('分词完成,用时{:.2f}s'.format((end - start)))


if __name__ == '__main__':
    calculate(word_segment, SolveFile, seg_Name)

