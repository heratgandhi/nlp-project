'''
Created on Feb 17, 2013

@author: jyotiPandey
'''

import re
from collections import Counter
'''
file operations
param: array of file names
'''

def addOneSmoothingUnigram(probability_dict, vocab_length, corpus_length):
    add_one_smooth = dict()
    for key,value in probability_dict.items():
        add_one_smooth[key] = (probability_dict[key] + 1) / (corpus_length + vocab_length)
    return add_one_smooth
    
    
def addOneSmoothingBigram(unigram_dict, probability_dict, vocab_length, corpus_length):
    add_one_smooth_bi = dict()
    for key,value in probability_dict.items():
        add_one_smooth_bi[key] = float(value + 1.0) / (float(unigram_dict[key.split()[0]]) + vocab_length)
    return add_one_smooth_bi
    
def file_operations(filenames):
    # process each file individually
    for filename in filenames:
        #open file in read mode
        
        lines = open(filename, 'r').read()
        sentences = re.compile(r'(?<=[.!?;])\s*').split(lines)
        sentences_with_tag = '';
        
        for sentence in sentences:
            sentences_with_tag += ' <s> '+sentence+' </s> '
        words = sentences_with_tag.split()
        
        unigram_dict = dict(Counter(words).items())
        len_unigram = len(unigram_dict)
         
        unigram_prob = dict(unigram_dict)
        for key, value in unigram_prob.items():
            unigram_prob[key] = float(value/len_unigram)
        
        print ("******************ADD ONE SMOOTHING OF UNIGRAM***********************")
        unigram_prob_smooth_1 = addOneSmoothingUnigram(unigram_prob, len_unigram, words.__len__())
        for unigram,prob in unigram_prob_smooth_1.items():
            print (unigram, '\t\t' , prob)
        
        #this method of making bigrams is wrong because we have to consider 0 counts too
        index_r = 0
        bi_words = words
        while index_r < len(bi_words):
            if index_r + 1 < len(bi_words):
                bi_words[index_r] += " " + bi_words[index_r+1]
            index_r += 1
        
        bigram_dict = dict(Counter(bi_words).items())
        len_bigram = len(bigram_dict)
        
        bigram_prob = dict(bigram_dict)
        print ("******************ADD ONE SMOOTHING OF BIGRAM***********************")
        for key,value in bigram_prob.items():
            key1 = key.split()[0]
            bigram_prob[key] = value / float(unigram_dict[key1])
             
        bigram_prob_smooth_1 = addOneSmoothingBigram(unigram_dict, bigram_prob, len_unigram, words.__len__())
        for key,value in bigram_prob_smooth_1.items() :
            print (key, '\t\t' ,value )
            
def main():
    file_operations(['small.txt'])
        
main()