# assignment1

##策略逻辑

本策略采用支持向量机的方法对沪深 300 指数进行择时。遵循全面性原则，本文选取了价量、资金等 22 个指标作为备选特征向量，根据相关系数矩阵，逐一剔除相关系数较强的指标，最终剩余 12 个指标，具体如下：换手率、ADTM、ATR、CCI、MACD、MTM、ROC、SOBV、STD26、STD5、两融交易额占 A 股成交额（%）、上一交易周收益率。
将 2013-01-01 至 2017-12-31 作为训练集，样本数据频率为周，共计 256周。在训练样本中，将下周周收益为正的定义为 1，下周周收益率为负的定义为 0。通过对核函数选择、对参数进行寻优，得到一个训练模型，对 2018 年 1 月 2 日至 2018 年 1 月 5 日进行预测，之后将训练样本长度增加一周，重新修正模型，再预测下一周。鉴于策略在未满五天的交易周之后的预测精准度相对较弱，对未满五天交易周之后一周的策略延续上一周操作，在此操作下策略表现相对更为优异。
