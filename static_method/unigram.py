#coding=gbk
import json
import time
from classes.Sentence_Network_Graph_Probability import SentenceNetworkGraph_Probability

from static_config import *


def get_dict():
    with open(Unigram_Dict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def unigram(sentence, word_dict):
    sngp = SentenceNetworkGraph_Probability(sentence,word_dict)
    result = sngp.solve()
    return result


print("正在获取词典...")
word_dictionary = get_dict()
print("词典获取完成")
print("开始分词")
times = 0
start = time.time()
with open(SolveFile, 'r', encoding='ansi') as solve_file:
    with open(seg_Unigram, 'w', encoding='ansi') as result_file:
        for sentence in solve_file:
            sentence = sentence.rstrip()
            if sentence == '':
                result_file.write('\n')
                continue
            word_list_FMM = unigram(sentence, word_dictionary)
            sentence_cut = ''
            for word in word_list_FMM:
                sentence_cut = sentence_cut + word + '/  '
            result_file.write(sentence_cut)
            result_file.write('\n')
            times += 1
            print("第{}个句子已完成分句".format(times))
end = time.time()
print('分词完成,用时{:.2f}s'.format((end - start)))
