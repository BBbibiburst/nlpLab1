# coding=gbk
import json
import re
from math import log
import sys
import time

from replace_dict import replace_dict
from status_config import *
import HMM.OOV_discover
from score import showscore, upper_get_score


def get_dict():
    with open(Bigram_Dict, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def get_probability(word_dict, word1, word2):
    # print(word1,' ',word2)
    probability_bigram = 0
    if word_dict[word1].get(word2) is not None:
        probability_bigram = linear_interpolation * word_dict[word1][word2] / word_dict[word1]['__len__']
    probability_unigram = (1 - linear_interpolation) * word_dict[''][word2] / word_dict['']['__len__']
    probability = probability_bigram + probability_unigram
    return log(probability)


def replace_back(sentence_cut, replace_list):
    for key, item_list in replace_list.items():
        for item in item_list:
            sentence_cut = sentence_cut.replace(key, item, 1)
    return sentence_cut


def find_max_value_pos(dp, pos):
    max_value = -sys.maxsize
    max_pos = pos - 1
    for k, v in dp[pos].items():
        if v > max_value:
            max_value = v
            max_pos = k
    return max_pos


def add_dict(word_dict, last_word, word, p):
    if word_dict.get(last_word) is None:
        word_dict[last_word] = {}
    if word_dict[last_word].get(word) is None:
        word_dict[last_word][word] = 10 ** -p
        if word_dict[last_word].get('__len__') is None:
            word_dict[last_word]['__len__'] = 1


def add_into_dict(sentence_cut, word_dict, p):
    sentence_cut.append('__End__')
    last_word = ''
    for i in sentence_cut:
        word = i
        add_dict(word_dict, last_word, word, p)
        add_dict(word_dict, '', word, p)
        last_word = word


def bigram(sentence, word_dict, OOV_param=(11, 11)):
    add_into_dict([i for i in sentence], word_dict, OOV_param[0])
    add_into_dict(HMM.OOV_discover.word_segment(sentence, HMM_dict), word_dict, OOV_param[1])
    # viterbi算法计算概率
    result = []
    sentence_length = len(sentence)
    dp = {d: {} for d in range(sentence_length + 1)}
    dp[0][0] = 0
    dp_back = {d: {} for d in range(sentence_length + 1)}
    minus_limit = -sys.maxsize >> 10
    for i in range(1, sentence_length + 1):
        for j in range(i):
            word2 = sentence[j:i]
            if word_dict[''].get(word2) is None:
                continue
            max_value = -sys.maxsize
            max_pos = 0
            for k, v in dp[j].items():
                word1 = sentence[k:j]
                if word_dict[''].get(word1) is None:
                    continue
                prob = get_probability(word_dict, word1, word2)
                value = v + prob
                if value > max_value:
                    max_value = value
                    max_pos = k
            if max_value > -sys.maxsize:
                dp[i][j] = max_value
                dp_back[i][j] = max_pos
    # 反向计算结果
    length = len(sentence)
    pos = find_max_value_pos(dp, length)
    last_pos = dp_back[length][pos]
    word = sentence[pos:]
    sentence = sentence[:pos]
    result.append(word)
    while sentence != '':
        length = len(sentence)
        pos = last_pos
        last_pos = dp_back[length][pos]
        word = sentence[pos:]
        sentence = sentence[:pos]
        result.insert(0, word)
    return result


def calculate(func, SolveFile, seg_gram, OOV_param=(14, 14)):
    print("正在获取词典...")
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
                word_list = func(sentence, word_dictionary, OOV_param)
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


word_dictionary = get_dict()
HMM_dict = HMM.OOV_discover.get_dict()
calculate(bigram, SolveFile, seg_Bigram)
sentence = '维尔茨堡是美因河畔的一座城堡。玛利恩堡（Festung Marienberg）是德国维尔茨堡美因河畔的一座城堡，它是维尔茨堡的象征，作为王子主教的家近5个世纪。自古以来这里就是一个要塞。大约1600年，朱利叶·埃希特（Julius Echter）将其重建成一个文艺复兴时期的宫殿堡垒。30年战争期间， 1631年瑞典古斯塔夫二世·阿道夫，堡垒于1657年改建为一个更强大的巴洛克式堡垒，一个王子公园布局形成。'
print(solve(sentence, bigram, word_dictionary))
sentence = '中共中央于10月24日上午10时举行新闻发布会，中共中央总书记习近平同志，中央政法委秘书长陈一新同志，中央政策研究室主任江金权同志，中央改革办分管日常工作的副主任、国家发展改革委副主任穆虹同志，中央纪委国家监委宣传部部长王建新同志，中央办公厅副主任兼调研室主任唐方裕同志，中央宣传部副部长孙业礼同志介绍解读党的二十大报告主要精神。李克强、栗战书、汪洋、李强、赵乐际、王沪宁、韩正、蔡奇、丁薛祥、李希、王岐山、马兴瑞、王晨、王毅、尹力、石泰峰、刘鹤、刘国中、许其亮、孙春兰、李干杰、李书磊、李鸿忠、杨晓渡、何卫东、何立峰、张又侠、张国清、陈文清、陈吉宁、陈敏尔、胡春华、袁家军、黄坤明、温家宝、贾庆林、张德江、俞正声、宋平、李岚清、曾庆红、吴官正、李长春、贺国强、刘云山、张高丽、刘金国、王小洪、杨洁篪、陈希、陈全国、郭声琨、尤权参加了会见。'
print(solve(sentence, bigram, word_dictionary))

