实验说明：

3.1 词典保存在results/dict.txt中

3.2 FMM和BMM分词结果分别为results/seg_FMM.txt和results/seg_BMM.txt 
源代码保存在physicial_method/phy.py和phy_utils.py中，phy_utils.py实现了Trie树，
phy.py调用phy_utils.py中的类和方法将FMM和BMM结果输出。

3.3 评分输出结果保存在results/score.txt中

3.4 分词程序的优化保存在physicial_method/phy_fixed1.py，phy_fixed2.py和phy_utils.py中
本次优化实现了哈希表，并利用哈希表优化了3.2的Trie树，phy_fixed1.py调用优化的Trie树，而phy_fixed2.py直接使用哈希表进行分词

3.5 实现了Bigram模型（集成了3.6中的未登录词识别模块和分词后处理）（不是最终提交的三个分词优化系统模型之一），保存在status_method/bigram.py中，输出结果为seg_LM,默认保存在results/seg_LM.txt。
bigram.py文件的末尾有详细的使用说明。

3.6 集成了未登录词识别的Bigram在3.5节status_method/bigram.py中，为了方便助教验收，将模型进行了集成。最终作为性能评分依据的三个模型分别为mix_model文件夹下的mix1.py，mix2.py，mix3
.py，三个模型在各自的文件末尾有详细的操作说明。为防止与Bigram的seg_LM.txt混淆，特将这三个模型的分词结果默认保存在mix_model文件夹下，即mix_model/seg_LM.txt
