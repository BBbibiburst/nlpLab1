# coding=gbk
import json
import time
from static_method.Sentence_Network_Graph_Unigram import SentenceNetworkGraph_Unigram

from static_config import *


def get_dict():
    with open(Unigram_Dict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def unigram(sentence, word_dict):
    sngp = SentenceNetworkGraph_Unigram(sentence, word_dict)
    result = sngp.solve()
    return result


def calculate(func,SolveFile,seg_gram):
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
                word_list = func(sentence, word_dictionary)
                sentence_cut = ''
                for word in word_list:
                    sentence_cut = sentence_cut + word + '/  '
                result_file.write(sentence_cut)
                result_file.write('\n')
                times += 1
                print("��{}����������ɷ־�".format(times))
    end = time.time()
    print('�ִ����,��ʱ{:.2f}s'.format((end - start)))


calculate(unigram,SolveFile,seg_Unigram)