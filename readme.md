实验说明：

3.1 词典保存在results/dict.txt中

3.2 FMM和BMM分词结果分别为results/seg_FMM.txt和results/seg_BMM.txt 
源代码保存在physicial_method/phy.py和phy_utils.py中，phy_utils.py实现了Trie树，
phy.py调用phy_utils.py中的类和方法将FMM和BMM结果输出。

3.3 评分输出结果保存在results/score.txt中

3.4 分词程序的优化保存在physicial_method/phy_fixed1.py，phy_fixed2.py和phy_utils.py中
本次优化实现了哈希表，并利用哈希表优化了3.2的Trie树，phy_fixed1.py调用优化的Trie树，而phy_fixed2.py直接使用哈希表进行分词


bigram改进：自动参数确定，词典删除,合并用BM