#!/usr/bin/env python
"""mapper.py"""
import sys, re, gensim
from gensim import corpora, models, similarities,utils 
import numpy as np
import pickle


for line in sys.stdin:
    words = line.split(' ')
    # increase counters
    number_of_ant = words[0]
    number_of_alha = words[1]
    number_of_eta = words[2]

    mm = corpora.mmcorpus.MmCorpus('/code/docword.enron.txt_.mm')

    lda = gensim.models.ldamodel.LdaModel(corpus=mm, num_topics=10,alpha=float(number_of_alha),
update_every=1, chunksize=2000, passes=1,eta=float(number_of_eta), decay=0.5, offset=1.0, eval_every=10, iterations=1000,
gamma_threshold=0.001, minimum_probability=0.01)
    perplex = lda.bound(mm)
    per_word_perplex = np.exp2(-perplex / sum(cnt for document in mm for _, cnt in document))
    print '{} {}'.format(words[0], per_word_perplex)
