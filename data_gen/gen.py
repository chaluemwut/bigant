from gensim import corpora, models, similarities,utils 

def gen_data(data_set_name):
    docword="docword.{}.txt".format(data_set_name)
    vocabulary="vocab.{}.txt".format(data_set_name)
    dictionary=corpora.ucicorpus.UciCorpus(docword,vocabulary)

    dictx=dictionary.create_dictionary() 
    corpora.mmcorpus.MmCorpus.serialize(docword + '_.mm', dictionary)

if __name__ == '__main__':
    gen_data('enron')
    gen_data('nips')

