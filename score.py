# coding=gbk
from physicial_method.phy_config import seg_FMM,seg_BMM,TrainingDataFile
from static_method.static_config import seg_Unigram
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
    line_split = re.findall(r'\[[^\[\]]*\]\S*|[^\[\]\s]*/\S*', line)
    pos = 0
    for word in line_split:
        if word[0] == '[':
            word_split = re.findall(r'[^\[\s]*/[^/\s\]]*', word)
            word = ''
            for c in word_split:
                word += getWord(c)
        else:
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


print("正在计算...")
#score1 = getTotalScore(TrainingDataFile[3:], seg_FMM[3:])
#score2 = getTotalScore(TrainingDataFile[3:], seg_BMM[3:])
score3 = getTotalScore(TrainingDataFile[3:], seg_Unigram[3:])
print("计算完成")
#print('FMM:\n精确率:{:.3f},召回率:{:.3f},F1值:{:.3f}'.format(score1[0],score1[1],score1[2]))
#print('BMM:\n精确率:{:.3f},召回率:{:.3f},F1值:{:.3f}'.format(score2[0],score2[1],score2[2]))
print('Unigram:\n精确率:{:.3f},召回率:{:.3f},F1值:{:.3f}'.format(score3[0],score3[1],score3[2]))
