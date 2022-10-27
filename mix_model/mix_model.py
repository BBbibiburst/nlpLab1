# coding=gbk
import json
import re
import time

from CBGM.CBGM import replace_back
from Tri_CBGM.Tri_CBGM import tri_cbgm
from physicial_method.Sentence_Network_Graph import SentenceNetworkGraph
from status_method.bigram import bigram
from config.mix_config import *
from replace_dict import *


def mix_get_dict(DictFile):
    with open(DictFile, 'r', encoding='ansi') as f:
        word_dict = json.load(f)
    return word_dict


bigram_dict = mix_get_dict(bigram_dict_file)
cbgm_dict = mix_get_dict(tri_cbgm_dict_file)


# ˫��ƥ��
def mix(sentence):
    bigram_result = bigram(sentence, bigram_dict)
    cbgm_result = tri_cbgm(sentence, cbgm_dict)
    sng = SentenceNetworkGraph(sentence, [cbgm_result,bigram_result])
    return sng.solve()


def solve(sentence):
    sentence = sentence.rstrip()
    if sentence == '':
        return ''
        ##
    replace_list = {i: [] for i in replace_dict.values()}
    for key, value in replace_dict.items():
        replace_list[value] = re.findall(key, sentence)
        sentence = re.sub(key, value, sentence)
        ##
    word_list = mix(sentence)
    sentence_cut = ''
    for word in word_list:
        sentence_cut = sentence_cut + word + '/  '
    sentence_cut = replace_back(sentence_cut, replace_list)
    return sentence_cut


def calculate(func):
    print("���ڻ�ȡ�ʵ�...")
    print("�ʵ��ȡ���")
    print("��ʼ�ִ�")
    times = 0
    start = time.time()
    with open(SolveFile, 'r', encoding='ansi') as solve_file:
        with open(seg_mix, 'w', encoding='ansi') as result_file:
            for sentence in solve_file:
                sentence = sentence.rstrip()
                if sentence == '':
                    result_file.write('\n')
                    continue
                    ##
                replace_list = {i: [] for i in replace_dict.values()}
                for key, value in replace_dict.items():
                    replace_list[value] = re.findall(key, sentence)
                    sentence = re.sub(key, value, sentence)
                    ##
                word_list = func(sentence)
                sentence_cut = ''
                for word in word_list:
                    sentence_cut = sentence_cut + word + '/  '
                sentence_cut = replace_back(sentence_cut, replace_list)
                result_file.write(sentence_cut)
                result_file.write('\n')
                times += 1
                print("��{}����������ɷ־�".format(times))
    end = time.time()
    print('�ִ����,��ʱ{:.2f}s'.format((end - start)))


if __name__ == '__main__':
    calculate(mix)
    sentence = 'ά���ı���������ϵ�һ���Ǳ������������ǵ¹�ά���ı�������ϵ�һ���Ǳ�������ά���ı�����������Ϊ�������̵ļҽ�5�����͡��Թ������������һ��Ҫ������Լ1600�꣬����Ҷ����ϣ�ؽ����ؽ���һ�����ո���ʱ�ڵĹ���ݡ�30��ս���ڼ䣬 1631������˹��������������򣬱�����1657��Ľ�Ϊһ����ǿ��İ����ʽ���ݣ�һ�����ӹ�԰�����γɡ�'
    print(solve(sentence))
    sentence = '�й�������10��24������10ʱ�������ŷ����ᣬ�й����������ϰ��ƽͬ־����������ί���鳤��һ��ͬ־�����������о������ν���Ȩͬ־������ĸ��ֹ��ճ������ĸ����Ρ����ҷ�չ�ĸ�ί�������º�ͬ־�������ί���Ҽ�ί����������������ͬ־������칫�������μ�����������Ʒ�ԣͬ־��������������������ҵ��ͬ־���ܽ�����Ķ�ʮ�󱨸���Ҫ�������ǿ����ս�顢������ǿ�����ּʡ������������������桢��Ѧ�顢��ϣ�����ɽ�����������������㡢������ʯ̩�塢���ס������С����������ﴺ������ɽܡ������ڡ�����ҡ������ɡ��������������塢���������Ź��塢�����塢�¼���������������������Ԭ�Ҿ������������¼ұ��������֡��ŵ½�������������ƽ������塢����졢�������������ع�ǿ������ɽ���Ÿ��������������С�顢���������ϣ����ȫ��������������Ȩ�μ��˻����'
    print(solve(sentence))
    sentence = '��ʥ�ڿ쵽�ˣ��������ƬҲ�ǳ�Ӧ����չʾ��һֻ�����顱��Ҳ���ǲ��޿�����Brockengespenst�������ܿ������죬�����޿����󲢷ǳ���Ȼ��������һλ�۲��߱�Ͷ������������Ʋ��ϵ���Ӱ�����޿�������ټ����������������ʱ�����ϱ���������ɽ�£����п������˵�Ŀ����������ֻҪ�������������޿�������Գ������κεط����ڵ¹�������ɽ���Ĳ��޿Ϸ壬���ش�˵Ũ��������ɽ���������û��1780�꣬Լ����������ʩ�����ڴ˹۲쵽�ˡ����顱�����������������¼������������Ϊ�����޿����󡱡�'
    print(solve(sentence))
    sentence = '��ʥ��ǰϦ��������һ��ǰ��λ��������������60Ӣ�ﴦ��һ�������С�����ǽ�����ȥ���������������һ������������16���ͻ�԰����������ž޴�ĵ��񣬾��Ծ��մ̼�����������Ƭ�У��¿�˹�ڶ����Ĵ������һ�ֱ�������Ԩ�ĸо����¿�˹�������ڤ��֮��Ҳ��Υ�����Եĳͷ��ߡ��������﹫԰�ﻹ����������ֵ��ĵ���������Ⱥʨ����������˺���ˣ�����εĴ���ץ������ʿ������Щ��������500�����ʷ����������Ȼ�����Ƿ������ĸе��־壬��������������԰�ı��⡣16���Ͳ��������ŷ˹�ṫ����ʹʧ���޺�ί���˽�����������԰��'
    print(solve(sentence))
    sentence = '������֮���Գ�Ϊ���������ŵ��������ںܴ�̶���Ҫ�鹦������ϲ����ͯ�����¡���СѼ�������½�����һֻ��׾��ª��Ѽ�ӣ���������Լ���һֻ�����İ���졣���������֪�Ĺ��¾���������̽�ֳɳ��ɱ�����ı��ʡ������ں�������Ȼ������������ֻ������ë�İ���죬�Ͳ�������Ϊʲô��ҳ�˵�������һ�����š��ˡ�'
    print(solve(sentence))
    sentence = '�����������ڶ�ֺ������˵�ǡ���ֺ��������ʵ�ǡ���ָ�������ǵ�˫�ۣ�ǰ�㣩���ж�ֺ��������������ֺ������ͬ���ȴ������������������ֺ��������ֺ����ȴ��Զ�ס�����������Ƭ�����ڸ�˹����ӵ�һ������С����Ƭ�е�ĸ������Ȼ���ܣ������ǲ�����Զ��һ����Ϊ��������õ�������Ƕ��ӡ������������ٺͱ�������򽻵�����������ʱ�������������һ������档'
    print(solve(sentence))
    sentence = 'Ⱥ��������һ����͸�����⿴��ȥ���񻰹��»�ƻ�ʷʫ��ĳ�����������������й������콭�羰��ȴ����ʵ���ڵġ������콭�羰�����й����ܻ�ӭ����Ȼ����֮һ���콭�����õ����Ŀ�˹�ص�ò����˹�ص�ò����������ط����ڲ�ͬ�ĵ�����������ߴ����Ե��Ǹ�����ïʢֲ����׶״ɽ������صĵ��º��ܶ���'
    print(solve(sentence))
    sentence = '��ҶƮ�䣬��������Ȼ�߽�����������ڣ����ǻ��뵽�����޺͵�о�ޣ��뵽�Ϲ����Ϻ��޻��ǡ������������ʵİ������ˬ��ҹ���߳����ţ�ȥ�����⾡Ⱦ���ְɡ�˵����Ҷ��������Ϊ��Ӣ�����ķ���������Ҳ������Ϊ���ɽ���İ���������ϲ��İ���������ѡ����죬�������ݵ�����ɼ�����˲��õĽ�ɫ����ɫ�����ɫ���󲿷ְ�����Ҷ�����ļ�����ģ�������ɼ����Ҷȴ�ǻ���ġ�����ɼ����ë״ҶƬ�������ɺ���ɫ���ڶ������£�Ȼ���ڴ��쳤���µ���Ҷ������ɼԭ�����������ϲ�����ī�������ذ����������Ⱥ�����ïʢ������������·��˹�����ݵĺ���ܳ�����Ҳ�����ڴ������в����غ�ƽԭ�����������Ƭ����ƬѤ����С���֡�����ɼ�ںӰ�������ȳ�ʪ��������׳�ɳ�����������������ȴ�ܳ���100Ӣ�����ϣ�Ϊ���ܶ������������ṩ����Ҫ����Ϣ�أ�������������������ʴ���������������������������ݣ���������ɼ��Ҷǰ��ȥ���������������������ɡ�'
    print(solve(sentence))
