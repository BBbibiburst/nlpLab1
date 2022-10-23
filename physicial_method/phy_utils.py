# coding=gbk

import re
import time

from phy_config import *
from Sentence_Network_Graph import SentenceNetworkGraph
from Trie_Tree import *
from replace_dict import *


# 获取词典
def get_dict(class_name):
    word_dict = class_name()
    with open(DictFile, "r", encoding='ansi') as dict_file:
        for line in dict_file:
            line = line.rstrip()
            word_dict.insert(line)
    return word_dict


# 正向最大匹配
def FMM(sentence, word_dict):
    result = []
    maxlength = len(sentence)
    while True:
        sentence_length = len(sentence)
        if maxlength == 0 and sentence_length != 0:
            result.append(sentence)
            break
        if maxlength == 0 and sentence_length != 0:
            result.append(sentence)
            break
        if sentence_length == 0:
            break
        word_cut = sentence[0:maxlength]
        if word_dict.get(word_cut):
            result.append(word_cut)
            sentence = sentence[maxlength:]
            maxlength = sentence_length
        else:
            maxlength -= 1
    return result


# 逆向最大匹配
def BMM(sentence, word_dict):
    result = []
    maxlength = len(sentence)
    while True:
        sentence_length = len(sentence)
        if maxlength == 0 and sentence_length != 0:
            result.insert(0, sentence)
            break
        if sentence_length == 0:
            break
        if maxlength > sentence_length:
            maxlength = sentence_length
        word_cut = sentence[-maxlength:]
        if word_dict.get(word_cut):
            result.insert(0, word_cut)
            sentence = sentence[:-maxlength]
            maxlength = sentence_length
        else:
            maxlength -= 1
    return result


# 双向匹配
def BM(sentence, word_dict):
    FMM_result = FMM(sentence, word_dict)
    BMM_result = BMM(sentence, word_dict)
    sng = SentenceNetworkGraph(sentence, [FMM_result, BMM_result])
    return sng.solve()


def replace_back(sentence_cut, replace_list):
    for key, item_list in replace_list.items():
        for item in item_list:
            sentence_cut = sentence_cut.replace(key, item, 1)
    return sentence_cut


def main(class_name):
    print("正在获取词典...")
    word_dictionary = get_dict(class_name)
    print("词典获取完成")
    print("开始分词")
    times = 0
    start = time.time()
    with open(SolveFile, 'r', encoding='ansi') as solve_file:
        with open(seg_BMM, 'w', encoding='ansi') as result_file_BMM:
            with open(seg_FMM, 'w', encoding='ansi') as result_file_FMM:
                for sentence in solve_file:
                    sentence = sentence.rstrip()
                    if sentence == '':
                        result_file_FMM.write('\n')
                        result_file_BMM.write('\n')
                        continue
                        ##
                    replace_list = {i: [] for i in replace_dict.values()}
                    for key, value in replace_dict.items():
                        replace_list[value] = re.findall(key, sentence)
                        sentence = re.sub(key, value,sentence)
                        ##
                    word_list_FMM = FMM(sentence, word_dictionary)
                    word_list_BMM = BMM(sentence, word_dictionary)
                    sentence_cut_FMM = ''
                    sentence_cut_BMM = ''
                    for word in word_list_FMM:
                        sentence_cut_FMM = sentence_cut_FMM + word + '/  '
                    for word in word_list_BMM:
                        sentence_cut_BMM = sentence_cut_BMM + word + '/  '
                    sentence_cut_FMM = replace_back(sentence_cut_FMM, replace_list)
                    sentence_cut_BMM = replace_back(sentence_cut_BMM, replace_list)
                    result_file_FMM.write(sentence_cut_FMM)
                    result_file_FMM.write('\n')
                    result_file_BMM.write(sentence_cut_BMM)
                    result_file_BMM.write('\n')
                    times += 1
                    print("第{}个句子已完成分句".format(times))
    end = time.time()
    print('分词完成,用时{:.2f}s'.format((end - start)))
