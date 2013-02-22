'''
Created on Feb 17, 2013

@author: Jyoti Pandey, Herat Gandhi
'''

import re
import operator
import random
from collections import Counter
from collections import OrderedDict
from operator import itemgetter

'''
file operations
param: array of file names
'''

def addOneSmoothingBigram(unigram_dict, probability_dict, vocab_length):
    add_one_smooth_bi = dict()
    for key,value in probability_dict.items():
        add_one_smooth_bi[key] = float(value + 1.0) / (float(unigram_dict[key.split()[0]]) + vocab_length)
    return add_one_smooth_bi

def randomSentenceGenerator(unigram_dict,text,vocab_length,bigram_prob,model):
    sentence = ''
    max_prob = unigram_dict[max(unigram_dict, key = lambda x: unigram_dict.get(x) )]
    
    if model == 1:
        print('unigram model for sentence generation')
        while (not '</s>' in sentence):
            random_p = random.uniform(0.0,max_prob+0.5)
            for key,value in unigram_dict.items():
                if value > random_p - 0.001 and value < random_p + 0.001:
                    sentence += ' ' + key
    else:
        print('bigram model for sentence generation')
        while (not '</s>' in sentence):
            if len(sentence) > 30:
                break
            random_p = random.uniform(0,1)
            if not '<s>' in sentence:
                for key,value in bigram_prob.items():
                    if ('<s>' == key.split()[0]) and (value >= random_p - 0.05 and value <= random_p + 0.05) :
                        sentence += key
                        break
            else:
                lastword = sentence.split()[-1]
                for key,value in bigram_prob.items():
                    if (lastword == key.split()[0]) and (value >= random_p - 0.05 and value <= random_p + 0.05) :
                        sentence += ' ' + key.split()[1]
                        break
    sentence = re.sub('<[^<]+>', "", sentence)
    return sentence
        
def probfinder(sentence,text,unigram_dict,perplexity,smoothing,vocab_length):
    if not perplexity:
        sentence = '<s> ' + sentence + ' </s>'
    words = sentence.split()
    
    index = 0
    while index < len(words)-1:
        words[index] += ' ' + words[index+1]
        index += 1
    words.pop()
    prob = 1
    
    for word in words:
        if word.split()[0] in unigram_dict.keys():
            if smoothing:
                prob *= float(text.count(word) + 1.0) / (float(unigram_dict[word.split()[0]]) + vocab_length)
            else:
                prob *= float(text.count(word)) / float(unigram_dict[word.split()[0]])
        else:
            continue
    
    print(prob)    
        
    if not perplexity:
        return prob
    else:
        if prob != 0:
            return float(1/prob) ** float(1/len(sentence))
        else:
            return 0
    
def file_operations(filenames):
    sentences_with_tag = ''
    
    for filename in filenames:
        lines = open(filename, 'r').read()
        lines = re.sub('<[^<]+>', "", lines)
        sentences = re.compile(r'(?<=[.!?;])\s*').split(lines)
        
        for sentence in sentences:
            sentences_with_tag += ' <s> '+sentence+' </s> '
    words = sentences_with_tag.split()
    unigram_dict = dict(Counter(words).items())
    
    len_unigram = len(unigram_dict)
     
    unigram_prob = dict(unigram_dict)
    for key, value in unigram_prob.items():
        unigram_prob[key] = float(value/len_unigram)
    
    '''bi_words = []
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
         
    bigram_prob_smooth_1 = addOneSmoothingBigram(unigram_dict, bigram_dict, len_unigram)'''
    index_r = 0
    bi_words = words
    while index_r < len(bi_words):
        if index_r + 1 < len(bi_words):
            bi_words[index_r] += " " + bi_words[index_r+1]
        index_r += 1
        
    bigram_dict = dict(Counter(bi_words).items())
    len_bigram = len(bigram_dict)
    bigram_prob = dict(bigram_dict)
    for key,value in bigram_prob.items():
        key1 = key.split()[0]
        bigram_prob[key] = value / float(unigram_dict[key1])
    
    print(probfinder('here you go', sentences_with_tag, unigram_dict,True,True,len_unigram))
    unigram_prob = dict(sorted(unigram_prob.items(), key=itemgetter(1),reverse = True))
    
    '''for i in range(5):
        print(str(i+1) + " " + randomSentenceGenerator(unigram_prob, sentences_with_tag, len_unigram, bigram_prob,2))'''

def main():
    file_operations(['wsj/wsj.train'])

def authorPrediction(filenames):
    text = ''
    email = dict()
    i = 1
    for filename in filenames:
        f = open(filename, 'r')
        for line in f:
            l1 = line.split()[0]
            l2 = ' '.join(line.split()[1:])
            if l1 in email.keys():
                email[l1] += ' '+l2
            else:
                email[l1] = l2
    for k,v in email.items():
        email[k] = set(v.split())
    print(email)          
#main()
authorPrediction(['EnronDataset/train.txt'])