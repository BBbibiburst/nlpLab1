# coding=gbk
from physicial_method.phy_config import TrainingDataFile
from status_method.status_config import seg_Bigram
import re


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


def getInterval_answer(line, text):
    interval = []
    line_split = re.findall(r'[^\[\[\s]*/[^\[\]\s]*',line)
    pos = 0
    for word in line_split:
        word = getWord(word)
        interval.append((pos, pos + len(word) - 1))
        pos += len(word)
    return interval


def getInterval_result(line, text):
    interval = []
    line_split = line[:-1].split('/  ')[:-1]
    pos = 0
    for word in line_split:
        interval.append((pos, pos + len(word) - 1))
        pos += len(word)
    return interval


def getSore(answer_interval, result_interval):
    answer = set(answer_interval)
    result = set(result_interval)
    answer_and_result = answer & result
    return len(answer_and_result), len(answer), len(result)


def getTotalScore(AnswerName, ResultName):
    answer_and_result = 0
    answer = 0
    result = 0
    with open(AnswerName, 'r', encoding='ansi') as answer_file:
        with open(ResultName, 'r', encoding='ansi') as result_file:
            for answer_line in answer_file:
                result_line = result_file.readline()
                text = getText(result_line)
                answer_interval = getInterval_answer(answer_line, text)
                result_interval = getInterval_result(result_line, text)
                score = getSore(answer_interval, result_interval)
                answer_and_result += score[0]
                answer += score[1]
                result += score[2]
    precision = answer_and_result / result
    recall = answer_and_result / answer
    F1 = 2 * precision * recall / (precision + recall)
    return precision, recall, F1


print("���ڼ���...")
score = getTotalScore(TrainingDataFile, seg_Bigram)
print("�������")
print('Bigram:\n��ȷ��:{:.3f},�ٻ���:{:.3f},F1ֵ:{:.3f}'.format(score[0], score[1], score[2]))

