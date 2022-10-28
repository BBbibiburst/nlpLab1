# coding=gbk
import json
import re
import time

from CBGM.CBGM import replace_back
from Tri_CBGM.Tri_CBGM import tri_cbgm
from config.post_process_config import Mix_Rule_Dict
from physicial_method.Sentence_Network_Graph import SentenceNetworkGraph
from post_process.post_process import post_process, get_rule_dict
from status_method.bigram import bigram
from config.mix_config import *
from replace_dict import *


def mix_get_dict(DictFile):
    with open(DictFile, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


bigram_dict = mix_get_dict(bigram_dict_file)
cbgm_dict = mix_get_dict(tri_cbgm_dict_file)



def get_word_list_result(sentence, status_list):
    result = []
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


def get_status_list(word_list):
    status_list = ''
    for word in word_list:
        word_len = len(word)
        if word_len == 1:
            status_list += 'S'
        else:
            for i in range(word_len):
                if i == 0:
                    status_list += 'B'
                elif i == word_len - 1:
                    status_list += 'E'
                else:
                    status_list += 'M'
    return status_list


# 双向匹配
def mix(sentence):
    bigram_result = bigram(sentence, bigram_dict)
    cbgm_result = tri_cbgm(sentence, cbgm_dict)
    sng = SentenceNetworkGraph(sentence, [bigram_result, cbgm_result])
    result = sng.solve()
    status_list = get_status_list(result)
    status_list = post_process(sentence, status_list, rule_dict)
    result = get_word_list_result(sentence, status_list)
    return result


def solve(sentence):
    sentence = sentence.rstrip()
    if sentence == '':
        return ''
        ##
    replace_list = {i: [] for i in replace_dict.values()}
    for key, value in replace_dict.items():
        replace_list[value] = re.findall(key, sentence)
        sentence = re.sub(key, value, sentence)
        ##
    word_list = mix(sentence)
    sentence_cut = ''
    for word in word_list:
        sentence_cut = sentence_cut + word + '/  '
    sentence_cut = replace_back(sentence_cut, replace_list)
    return sentence_cut


def calculate(func,SolveFile,seg_mix):
    print("正在获取词典...")
    print("词典获取完成")
    print("开始分词")
    times = 0
    start = time.time()
    with open(SolveFile, 'r', encoding='ansi') as solve_file:
        with open(seg_mix, 'w', encoding='ansi') as result_file:
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
                word_list = func(sentence)
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


rule_dict = get_rule_dict(Mix_Rule_Dict)
if __name__ == '__main__':
    calculate(mix, SolveFile,seg_mix)


