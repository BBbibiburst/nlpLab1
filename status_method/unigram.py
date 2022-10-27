# coding=gbk
import json
import re
import time

from replace_dict import replace_dict
from status_method.Sentence_Network_Graph_Unigram import SentenceNetworkGraph_Unigram

from config.status_config import *


def get_dict():
    with open(Unigram_Dict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def unigram(sentence, word_dict):
    sngp = SentenceNetworkGraph_Unigram(sentence, word_dict)
    result = sngp.solve()
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


calculate(unigram, SolveFile, seg_Unigram)
