# coding=gbk
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from mix_model import *


def mix(sentence):
    bigram_result0 = bigram(sentence, bigram_dict, mode=0)
    bigram_result1 = bigram(sentence, bigram_dict, mode=1)
    cbgm_result = tri_cbgm(sentence, cbgm_dict)
    sng = SentenceNetworkGraph(sentence, [bigram_result0, bigram_result1, cbgm_result])
    result = sng.solve()
    status_list = get_status_list(result)
    status_list = post_process(sentence, status_list, rule_dict)
    result = get_word_list_result(sentence, status_list)
    return result


if __name__ == '__main__':
    # 用法：
    # calculate(分词方法, 待分词文件路径, 分词结果文件路径)
    # 可以通过修改这个方法的参数，分词文件位置SolveFile（要写相对路径）调节要进行分词的文件，
    # SolveFile默认为resources/199801_sent.txt，分词结果保存在seg_mix = "seg_LM.txt"中，即本文件夹下。
    # eg. calculate(mix, r'../resources/199801_sent.txt', seg_mix)
    # 对相对路径在r'../resources/199801_sent.txt'的文件199801_sent.txt 进行分词，结果保存在本文件夹下的seg_LM.txt中。
    calculate(mix, sys.argv[1], sys.argv[2])
