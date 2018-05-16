# test LDA 
from gensim import corpora, models, similarities,utils 
import re
 
             

stoplist = set(line.strip() for line in open('stoplist.txt'))
#dictionary = corpora.Dictionary(line.lower().split()  for line in open('twitter2Mb.txt'))
#################################################
aline=[]
for line in open('testdata01.txt'):
     line=re.sub('<[^>]+>', '', line)
     utils.lemmatize(line)
     aline.append(line.lower().split())
    
################################################
dictionary = corpora.Dictionary(aline)
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
             if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
dictionary.compactify() # remove gaps in id sequence after words that were removed
print(dictionary)
#print(dictionary.token2id)
#lemmatize('Hello World! How is it going?! Nonexistentword, 21')

class MyCorpus(object):
     def __iter__(self):
         #for line in open('ebola-raw.txt'):
        for line in open('testdata01.txt'):
         #for line in open('twitter2Mb.txt'):
             line=re.sub('<[^>]+>', '', line)
             utils.lemmatize(line)
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(line.lower().split())
             
             
corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
corpus = MyCorpus()

corpora.MmCorpus.serialize('corpus007.mm', corpus)

import logging, gensim, bz2 ,numpy as np
mm = gensim.corpora.MmCorpus('corpus007.mm')
#print(mm)


#loop01

lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=10,alpha=1.0,
update_every=1, chunksize=2000, passes=1,eta=1.0, decay=0.5, offset=1.0, eval_every=10, iterations=1000,
gamma_threshold=0.001, minimum_probability=0.01)

for i in range(0, lda.num_topics):
    print 'Topic:: '+str(i) +' '+lda.print_topic(i)

perplex = lda.bound(mm)
print "Perplexity: %s" % perplex
#grid[0].append(perplex)
    
per_word_perplex = np.exp2(-perplex / sum(cnt for document in mm for _, cnt in document))
print "Per-word Perplexity: %s" % per_word_perplex
#grid[0].append(per_word_perplex)
