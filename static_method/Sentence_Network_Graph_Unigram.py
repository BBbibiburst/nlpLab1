import math
import sys


def probability(x):
    return math.exp(-x)


class SentenceNetworkGraph_Unigram:
    def __init__(self, sentence, word_dict):
        self.sentence = sentence
        self.sentence_length = len(sentence)
        self.link_list = [[[i + 1, 1]] for i in range(self.sentence_length + 1)]
        for i in range(self.sentence_length):
            for j in range(i + 1, self.sentence_length + 1):
                word = sentence[i:j]
                prob = word_dict.get(word)
                if prob is not None:
                    if j == i + 1:
                        self.link_list[i][0] = [j, prob]
                    else:
                        self.link_list[i].append([j, probability(prob)])

        self.link_list[self.sentence_length] = []

    def __dijkstra(self):
        visited = [0 for i in range(self.sentence_length + 1)]
        path = [-1 for i in range(self.sentence_length + 1)]
        dist = [sys.maxsize for i in range(self.sentence_length + 1)]
        dist[0] = 0
        while True:
            min_pos = -1
            length_max = sys.maxsize
            for pos, value in enumerate(dist):
                if value <= length_max and visited[pos] == 0:
                    length_max = value
                    min_pos = pos
            if min_pos == -1:
                break
            visited[min_pos] = 1
            for node in self.link_list[min_pos]:
                if visited[node[0]] == 0:
                    if dist[min_pos] + node[1] < dist[node[0]]:
                        dist[node[0]] = dist[min_pos] + node[1]
                        path[node[0]] = min_pos
        return path

    def solve(self):
        path = self.__dijkstra()
        result = []
        end = len(path) - 1
        while end != 0:
            start = path[end]
            result.insert(0, self.sentence[start:end])
            end = start
        return result
