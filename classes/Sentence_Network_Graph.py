import sys


class SentenceNetworkGraph:
    def __init__(self, sentence, word_cut_results):
        self.word_cut_results = word_cut_results
        self.sentence = sentence
        self.sentence_length = len(sentence)
        self.link_list = [[] for i in range(self.sentence_length + 1)]
        for i in range(self.sentence_length):
            self.link_list[i].append([i + 1, 1])
        for word_cut_result in word_cut_results:
            pos = 0
            for word in word_cut_result:
                word_length = len(word)
                node_flag = 0
                for node in self.link_list[pos]:
                    if node[0] == pos+word_length:
                        node_flag = 1
                if node_flag == 0:
                    self.link_list[pos].insert(0,[pos + word_length, 1])
                pos += word_length

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
            result.insert(0,self.sentence[start:end])
            end = start
        return result

