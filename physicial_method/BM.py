# coding=gbk
from phy_utils import *

print("���ڻ�ȡ�ʵ�...")
word_dictionary = get_dict(HashTable)
print("�ʵ��ȡ���")
print("��ʼ�ִ�")
times = 0
start = time.time()
with open(SolveFile, 'r', encoding='ansi') as solve_file:
    with open(seg_BM, 'w', encoding='ansi') as result_file_BM:
        for sentence in solve_file:
            sentence = sentence.rstrip()
            if sentence == '':
                result_file_BM.write('\n')
                continue
                ##
            replace_list = {i: [] for i in replace_dict.values()}
            for key, value in replace_dict.items():
                replace_list[value] = re.findall(key, sentence)
                sentence = re.sub(key, value, sentence)
                ##
            word_list_BM = BM(sentence, word_dictionary)
            sentence_cut_BM = ''
            for word in word_list_BM:
                sentence_cut_BM = sentence_cut_BM + word + '/  '
            sentence_cut_BM = replace_back(sentence_cut_BM, replace_list)
            result_file_BM.write(sentence_cut_BM)
            result_file_BM.write('\n')
            times += 1
            print("��{}����������ɷ־�".format(times))
end = time.time()
print('�ִ����,��ʱ{:.2f}s'.format((end - start)))
