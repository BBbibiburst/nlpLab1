# coding=gbk
import json


def get_rule_dict(File):
    with open(File, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


def post_process(sentence, status_list, rule_dict):
    first = ' '
    second = ' '
    for i in range(len(sentence)):
        if rule_dict.get(first) is None or rule_dict[first].get(second) is None:
            first = second
            second = sentence[i] + ' ' + status_list[i]
            continue
        for key in rule_dict[first][second].keys():
            if sentence[i:].startswith(key):
                if status_list[i+len(key)-1] in 'ES':
                    if i + len(key) > len(sentence):
                        status_list = status_list[:i] + rule_dict[first][second][key]
                    else:
                        status_list = status_list[:i] + rule_dict[first][second][key] + status_list[i+len(key):]
                    print('已进行后处理')
        first = second
        second = sentence[i] + ' ' + status_list[i]
    return status_list