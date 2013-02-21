'''
Created on Feb 17, 2013

@author: Jyoti Pandey, Herat Gandhi
'''

import re
from collections import Counter

'''
file operations
param: array of file names
'''

def addOneSmoothingBigram(unigram_dict, probability_dict, vocab_length):
    add_one_smooth_bi = dict()
    for key,value in probability_dict.items():
        add_one_smooth_bi[key] = float(value + 1.0) / (float(unigram_dict[key.split()[0]]) + vocab_length)
    return add_one_smooth_bi
    
def file_operations(filenames):
    
    for filename in filenames:
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
        
        bi_words = []
        for key,value in unigram_dict.items():
            for key1,value1 in unigram_dict.items():
                bi_words.append(key + " " + key1)
        
        bigram_dict = dict()
        for bi_word in bi_words:
            bigram_dict[bi_word] = sentences_with_tag.count(bi_word)
        
        len_bigram = len(bigram_dict)
        
        bigram_prob = dict(bigram_dict)
        for key,value in bigram_prob.items():
            key1 = key.split()[0]
            bigram_prob[key] = value / float(unigram_dict[key1])
             
        bigram_prob_smooth_1 = addOneSmoothingBigram(unigram_dict, bigram_dict, len_unigram)

def main():
    file_operations(['small.txt'])
        
main()