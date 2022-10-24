from enum import Enum

TrainingDataFile = [r'../resources/199801_seg&pos.txt', r'../resources/199802.txt', r'../resources/199803.txt',r'../resources/name_cut.txt']
ProbDict = r'../results/prob_dict.txt'
name_set = r'../resources/name_gbk.txt'
NameTrainSet = r'../resources/name_cut.txt'
NameProbDict = r'../results/name_prob_dict.txt'
first_name_set = r'../resources/first_name.txt'
SolveFile = r'../resources/199801_sent.txt'
seg_HMM = r'../results/seg_HMM.txt'
seg_Name = r'../results/seg_Name.txt'
include_seperated_words = False
minus_limit = -1000000


class Status(Enum):
    B = 'B'
    M = 'M'
    E = 'E'
    S = 'S'

class NameStatus(Enum):
    B = 'B'
    M = 'M'
    E = 'E'
    S = 'S'
    O = 'O'
