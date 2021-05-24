# -*- coding: utf-8 -*-
"""LDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t7COSp74zYrui5jnxhKcY2WhvizWGNGY
"""

# 在colab中，切换到工作目录
import os
if "news.txt" not in os.listdir():
    os.chdir('drive/MyDrive/LDA')
assert "news.txt" in os.listdir()

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

np.random.seed(2020) # 固定随机种子

marks = ",.!~`+-_=—“”‘’()[]\n"
stop_words = ["i","the",'in',"to","of","and","or","for","on","that","he",
"she","it","is","was","were","his","mr","with","you","from","a","an","no","not",
"at","but","as","are","be","has","have","we","who","they","by","had","would",
"its","their","which","this","said","about","my","been","her","after","one",
"will","there","ms","when","what","after","new","more","if","also","than",
"him","them","so","me","some","other","all","can","could"]


# 数据预处理
dataset = []
with open("./news.txt",'r',encoding='utf-8') as file:
  lines = file.readlines()
for line in lines:
  # 统一小写
  new_line = line.lower()
  # 去除标点
  for mk in marks:
      new_line = new_line.replace(mk,' ')
  # 去除stop_words
  new_line = new_line.split()
  words = [w for w in new_line if w not in stop_words and len(w)>1]
  dataset.append(' '.join(words))


# 获取词频向量
cntVector = CountVectorizer()
cntTf = cntVector.fit_transform(dataset)
vocs = cntVector.get_feature_names()
print('词袋大小：', len(vocs))


for k in [5,10,20]:
  print("=====主题数: %d====="%k)
  lda = LatentDirichletAllocation(n_components=k,
                    max_iter=10,
                    random_state=2020) # 固定随机种子
  lda.fit_transform(cntTf)

  # 打印每个单词的主题的权重值
  tt_matrix = lda.components_
  id = 0
  for tt_m in tt_matrix:
    tt_m /= np.sum(tt_m)
    tt_dict=[(name, tt) for name, tt in zip(vocs, tt_m)]
    tt_dict=sorted(tt_dict, key=lambda x: x[1],reverse=True)
    # 打印每个类别前5个主题词：
    tt_dict = tt_dict[:10]
    print('主题%d:'%(id),tt_dict)
    id += 1