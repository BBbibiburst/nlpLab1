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
    # �÷���
    # calculate(�ִʷ���, ���ִ��ļ�·��, �ִʽ���ļ�·��)
    # ����ͨ���޸���������Ĳ������ִ��ļ�λ��SolveFile��Ҫд���·��������Ҫ���зִʵ��ļ���
    # SolveFileĬ��Ϊresources/199801_sent.txt���ִʽ��������seg_mix = "seg_LM.txt"�У������ļ����¡�
    # eg. calculate(mix, r'../resources/199801_sent.txt', seg_mix)
    # �����·����r'../resources/199801_sent.txt'���ļ�199801_sent.txt ���зִʣ���������ڱ��ļ����µ�seg_LM.txt�С�
    calculate(mix, sys.argv[1], sys.argv[2])
