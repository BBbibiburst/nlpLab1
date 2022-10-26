from enum import Enum

TrainingDataFile = [r'../resources/199801_seg&pos.txt',r'../resources/199802.txt', r'../resources/199803.txt']
# TrainingDataFile = [r'../resources/199801_seg&pos.txt']
ProbDict = r'../results/CBGM_prob_dict.txt'
SolveFile = r'../resources/199801_sent.txt'
seg_CBGM = r'../results/seg_CBGM.txt'
include_seperated_words = False
minus_limit = -1000000000


class Status(Enum):
    B = 'B'
    M = 'M'
    E = 'E'
    S = 'S'
