from enum import Enum

TrainingDataFile = [r'../resources/199801_seg&pos.txt', r'../resources/199802.txt', r'../resources/199803.txt']
# TrainingDataFile = [r'../resources/199801_seg&pos.txt']
ProbDict = r'../results/Tri_CBGM_prob_dict.txt'
SolveFile = r'../resources/199801_sent.txt'
NameTrainSet = r'../resources/name_cut.txt'
seg_CBGM = r'../results/seg_Tri_CBGM.txt'
include_seperated_words = False
minus_limit = -100000000


class Status(Enum):
    B = 'B'
    M = 'M'
    E = 'E'
    S = 'S'
