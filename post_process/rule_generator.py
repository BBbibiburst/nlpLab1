# coding=gbk
import json
import re
from config.post_process_config import *
from replace_dict import replace_dict


def getText(answer_line):
    text = ''
    words = answer_line.split("/  ")
    for word in words:
        text += word
    text.rstrip()
    return text


def getWord(word):
    word_split = word.split(r'/')
    word = ''
    for i in range(len(word_split)):
        if i != len(word_split) - 1:
            word += word_split[i] + '/'
    word = word[:-1]
    return word


def get_answer(line, text):
    interval = []
    line_split = re.findall(r'[^\[\[\s]*/[^\[\]\s]*', line)
    pos = 0
    for word in line_split:
        word = getWord(word)
        interval.append(text[pos: pos + len(word)])
        pos += len(word)
    return interval


def get_result(line, text):
    interval = []
    line += '  '
    line_split = line[:-1].split('/  ')[:-1]
    pos = 0
    for word in line_split:
        interval.append(text[pos: pos + len(word)])
        pos += len(word)
    return interval


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


def add_into_dict(rule_dict, first, second, sentence_solve, status_solve):
    if rule_dict.get(first) is None:
        rule_dict[first] = {}
    if rule_dict[first].get(second) is None:
        rule_dict[first][second] = {}
    if rule_dict[first][second].get(sentence_solve) is None:
        rule_dict[first][second][sentence_solve] = status_solve


def add_rules(sentence, answer, result, rule_dict):
    answer_list = get_status_list(answer)
    result_list = get_status_list(result)
    first = ' '
    second = ' '
    for i in range(len(sentence)):
        j = i
        sentence_solve = ''
        status_solve = ''
        end_flag = 0
        while answer_list[j] != result_list[j] or (status_solve != '' and status_solve[-1] not in 'ES'):
            sentence_solve += sentence[j]
            status_solve += answer_list[j]
            j += 1
            if j >= len(sentence):
                end_flag = 1
                break
            result_list = answer_list[:j] + result_list[j:]
        if end_flag == 0 and sentence_solve != '':
            add_into_dict(rule_dict, first, second, sentence_solve, status_solve)
        first = second
        second = sentence[i] + ' ' + answer_list[i]


def get_rules(rule_dict, AnswerName, ResultName):
    with open(AnswerName, 'r', encoding='ansi') as answer_file:
        with open(ResultName, 'r', encoding='ansi') as result_file:
            for answer_line in answer_file:
                result_line = result_file.readline()
                result_line = result_line[:-1]
                for key, value in replace_dict.items():
                    answer_line = re.sub(key, value, answer_line)
                    result_line = re.sub(key, value, result_line)
                text = getText(result_line)
                answer = get_answer(answer_line, text)
                result = get_result(result_line, text)
                add_rules(text, answer, result, rule_dict)
    return rule_dict


def make_dict(seg, Rule):
    rule_dict = {}
    rule_dict = get_rules(rule_dict, AnswerFile[0], seg[0])
    rule_dict = get_rules(rule_dict, AnswerFile[1], seg[1])
    rule_dict = get_rules(rule_dict, AnswerFile[2], seg[2])
    with open(Rule, 'w', encoding='ansi') as f:
        json_dump = json.dumps(rule_dict)
        f.write(json_dump)


if __name__ == "__main__":
    make_dict(seg_Tri_CBGM, Tri_CBGM_Rule_Dict)
    make_dict(seg_Bigram, Bigram_Rule_Dict)
    make_dict(seg_mix, Mix_Rule_Dict)
