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


# 双向匹配
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
    print("正在获取词典...")
    print("词典获取完成")
    print("开始分词")
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
                print("第{}个句子已完成分句".format(times))
    end = time.time()
    print('分词完成,用时{:.2f}s'.format((end - start)))


if __name__ == '__main__':
    calculate(mix)
    sentence = '维尔茨堡是美因河畔的一座城堡。玛利恩堡是德国维尔茨堡美因河畔的一座城堡，它是维尔茨堡的象征，作为王子主教的家近5个世纪。自古以来这里就是一个要塞。大约1600年，朱利叶·埃希特将其重建成一个文艺复兴时期的宫殿堡垒。30年战争期间， 1631年瑞典古斯塔夫二世·阿道夫，堡垒于1657年改建为一个更强大的巴洛克式堡垒，一个王子公园布局形成。'
    print(solve(sentence))
    sentence = '中共中央于10月24日上午10时举行新闻发布会，中共中央总书记习近平同志，中央政法委秘书长陈一新同志，中央政策研究室主任江金权同志，中央改革办分管日常工作的副主任、国家发展改革委副主任穆虹同志，中央纪委国家监委宣传部部长王建新同志，中央办公厅副主任兼调研室主任唐方裕同志，中央宣传部副部长孙业礼同志介绍解读党的二十大报告主要精神。李克强、栗战书、汪洋、李强、赵乐际、王沪宁、韩正、蔡奇、丁薛祥、李希、王岐山、马兴瑞、王晨、王毅、尹力、石泰峰、刘鹤、刘国中、许其亮、孙春兰、李干杰、李书磊、李鸿忠、杨晓渡、何卫东、何立峰、张又侠、张国清、陈文清、陈吉宁、陈敏尔、胡春华、袁家军、黄坤明、温家宝、贾庆林、张德江、俞正声、宋平、李岚清、曾庆红、吴官正、李长春、贺国强、刘云山、张高丽、刘金国、王小洪、杨洁篪、陈希、陈全国、郭声琨、尤权参加了会见。'
    print(solve(sentence))
    sentence = '万圣节快到了，今天的照片也非常应景，展示了一只“幽灵”，也就是布罗肯现象（Brockengespenst）。尽管看着灵异，但布罗肯现象并非超自然现象。这是一位观察者被投射在阳光对面云层上的阴影。布罗肯现象很少见，但如果你在黎明时分爬上薄雾弥漫的山坡，则有可能幸运地目睹这种现象。只要满足条件，布罗肯现象可以出现在任何地方。在德国哈尔茨山脉的布罗肯峰，当地传说浓雾弥漫的山间有幽灵出没。1780年，约翰·西尔伯施拉格在此观察到了“幽灵”，对其进行了描述记录，并将其命名为“布罗肯现象”。'
    print(solve(sentence))
    sentence = '万圣节前夕，跟我们一起前往位于罗马西北方向60英里处的一个意大利小镇。我们将带你去博马尔佐，那里有一个曾被遗忘的16世纪花园，里面陈列着巨大的雕像，绝对惊险刺激。在这张照片中，奥库斯黑洞洞的大嘴给人一种被吞入深渊的感觉，奥库斯是罗马的冥界之神，也是违背誓言的惩罚者。这座怪物公园里还有其他诡异怪诞的雕像，如龙被群狮攻击，巨人撕碎人，汉尼拔的大象抓走罗马士兵。这些雕像已有500年的历史，但它们仍然让人们发自内心感到恐惧，这或许就是这座公园的本意。16世纪博马尔佐的欧斯尼公爵在痛失爱妻后，委托人建造了这座公园。'
    print(solve(sentence))
    sentence = '疣鼻天鹅之所以成为美丽和优雅的象征，在很大程度上要归功于深受喜爱的童话故事《丑小鸭》。故事讲述了一只笨拙丑陋的鸭子，长大后发现自己是一只美丽的白天鹅。这个众所周知的故事经常被用于探讨成长蜕变和美的本质。当你在荷兰的自然保护区看到这只衔着羽毛的白天鹅，就不难明白为什么大家常说“像天鹅一样优雅”了。'
    print(solve(sentence))
    sentence = '霍氏树懒属于二趾树懒，说是“二趾”，但其实是“二指”：它们的双臂（前足）仅有二趾，但后足上有三趾。尽管同在热带雨林中享受慢生活，两趾树懒和三趾树懒却是远亲。今天这张照片拍摄于哥斯达黎加的一个海边小镇。照片中的母子俩虽然亲密，但它们不会永远在一起，因为树懒“最好的生活”就是独居。成年树懒很少和别的树懒打交道，不过，有时候雌性树懒会在一起挂着玩。'
    print(solve(sentence))
    sentence = '群峰像龙牙一样穿透薄雾。这看上去像神话故事或科幻史诗里的场景，但享誉世界的中国桂林漓江风景区却是真实存在的。桂林漓江风景区是中国最受欢迎的自然景点之一。漓江流经该地区的喀斯特地貌。喀斯特地貌赋予了这个地方与众不同的地质特征，最具代表性的是覆盖着茂盛植被的锥状山峰和奇特的地下河溶洞。'
    print(solve(sentence))
    sentence = '秋叶飘落，秋天已悄然走近。在这个季节，人们会想到法兰绒和灯芯绒，想到南瓜香料和棉花糖。让我们在晴朗的白天和凉爽的夜晚走出家门，去欣赏这尽染层林吧。说到秋叶，有人认为新英格兰的枫树最美，也有人认为洛基山脉的白杨或美国南部的柏树才是最佳。秋天，乔治亚州的落羽杉披上了灿烂的金色、橙色和深红色。大部分柏树的叶子是四季常青的，但落羽杉的树叶却是会掉的。落羽杉的羽毛状叶片在秋天变成红棕色，在冬天落下，然后在春天长出新的针叶。落羽杉原产于美国东南部，在墨西哥湾沿岸的密西西比河流域茂盛生长。它们在路易斯安那州的海湾很常见，也生长在大西洋中部的沿海平原，比如今天照片中这片绚丽的小树林。落羽杉在河岸和沼泽等潮湿环境中茁壮成长。它们生长缓慢，却能长到100英尺以上，为两栖动物、鱼类和鸟类提供了重要的栖息地，并保护海岸线免受侵蚀。如果你在这个季节来到乔治亚州，请在落羽杉落叶前，去欣赏它带来的秋日美景吧。'
    print(solve(sentence))
