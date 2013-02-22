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

def addOneSmoothingUnigram(probability_list, vocab_length, corpus_length):
    return [(ngram[0], float(ngram[1] + 1) /
             (corpus_length + vocab_length)) 
                for ngram in probability_list]
    
def addOneSmoothingBigram(unigram_dict, probability_list, vocab_length, corpus_length):
    return [(ngram[0], float(ngram[1] + 1.0) /
             (float(unigram_dict[ngram[0].split()[0]]) + vocab_length)) 
                for ngram in probability_list]

def wittenBellSmoothingBigram(ngram_list, words, corpus_data):
    witten_smooth_prob = {}
    for data in corpus_data:
        if(corpus_data[data][3] == 0):
            witten_smooth_prob[data] = float(corpus_data[data][0] / float(corpus_data[data][1] + corpus_data[data][2]))
        else :
            witten_smooth_prob[data] = float(corpus_data[data][3] / float(corpus_data[data][1] + corpus_data[data][2]))
    return witten_smooth_prob
    
def file_operations(filenames):
    # process each file individually
    for filename in filenames:
        #open file in read mode
        
        lines = open(filename, 'r').read()
        sentences = re.compile(r'(?<=[.!?;])\s*').split(lines)
        sentences_with_tag = '';
        
        for sentence in sentences:
            sentences_with_tag += ' <s> '+sentence+' </s> '
        # Split here for full stop and quotation marks
        words = sentences_with_tag.split()
        tempWordsList = sentences_with_tag.split()
        #Perform logic to save ---
        #1.    T(wi-1) - Vocab after wi-1
        #2.    N(wi-1) - Tokens after this
        #3.    Z(wi-1) - Number of bigrams in current 
        #      data set starting with wi-1 that do not occur in the training data
        
        #********************Vocab after wi-1************************
                       
        unigram_list = list(Counter(words).items())
        len_unigram = len(unigram_list)
         
        unigram_prob = unigram_list
        unigram_prob = [(unigram[0], float(unigram[1]/len_unigram)) for unigram in unigram_prob]
        print ("******************ADD ONE SMOOTHING OF UNIGRAM***********************")
        unigram_prob_smooth_1 = addOneSmoothingUnigram(unigram_prob, len_unigram, words.__len__())
        for unigram in unigram_prob_smooth_1:
            print (unigram[0], '\t\t' , unigram[1])
        
        index_r = 0
        bi_words = words
        while index_r < len(bi_words):
            if index_r + 1 < len(bi_words):
                bi_words[index_r] += " " + bi_words[index_r+1]
            index_r += 1
        
        bigram_list = list(Counter(bi_words).items())
        len_bigram = len(bigram_list)
        
        bigram_prob = bigram_list
        print ("******************ADD ONE SMOOTHING OF BIGRAM***********************")
        unigram_dict = {key: value for (key, value) in unigram_list}
        bigram_prob = [(bigram[0], bigram[1] / float(unigram_dict [bigram[0].split()[0]])) for bigram in bigram_prob]
        bigram_prob_smooth_1 = addOneSmoothingBigram(unigram_dict, bigram_prob, len_unigram, words.__len__())
        for bi in bigram_prob_smooth_1 :
            print (bi[0], '\t\t' , bi[1])
            
        print ("**********SMOOTHING OF WITTEN AND BELL SMOOTHING**************")
        list1 = {}
        n_vocab_length = len_unigram
        
        for i in range (0, len(words)):
            #Calculate the vocab after this word
            laterWords = list(Counter(tempWordsList).items())
            count = 0
            for first_word in bigram_list:
                if(first_word[0].split()[0] == words[i]):
                    count = count + 1
            list1[words[i]] = len(words) - i, len(laterWords), count , first_word[1]
            
            tempWordsList.pop()
        print (wittenBellSmoothingBigram(bigram_list, tempWordsList, list1))
        
def main():
    file_operations(['small.txt'])
        
main()