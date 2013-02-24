'''
Created on Feb 17, 2013

@author: Jyoti Pandey, Herat Gandhi, Vinayaka Dattatraya, Saikiran
'''

import re
import operator
import random
import math

from collections import Counter
from collections import OrderedDict
from operator import itemgetter

def printDictionary(my_dictionary):
    for key,value in my_dictionary.items():
        print(str(key) + ' : ' + str(value))
        
def addOneSmoothingBigram(unigram_dict, probability_dict, vocab_length):
    add_one_smooth_bi = dict()
    for key,value in probability_dict.items():
        add_one_smooth_bi[key] = float(value + 1.0) / (float(unigram_dict[key.split()[0]]) + vocab_length)
    return add_one_smooth_bi

def randomSentenceGenerator(unigram_dict,text,vocab_length,bigram_prob,model):
    sentence = ''
    max_prob = unigram_dict[max(unigram_dict, key = lambda x: unigram_dict.get(x) )]
    
    if model == 1:
        while (not '</s>' in sentence) and (len(sentence) < 30):
            random_p = random.uniform(0.0,max_prob+0.5)
            for key,value in unigram_dict.items():
                if value > random_p - 0.001 and value < random_p + 0.001:
                    sentence += ' ' + key
    else:
        while (not '</s>' in sentence):
            if len(sentence.split()) > 20:
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
        
def probfinder(sentence,text,unigram_dict,perplexity,smoothing,vocab_length,model):
    if not perplexity:
        sentence = '<s> ' + sentence + ' </s>'
    words = sentence.split()
    prob = 0
    
    if model == 2:
        index = 0
        while index < len(words)-1:
            words[index] += ' ' + words[index+1]
            index += 1
        words.pop()
        
        for word in words:
            if word.split()[0] in unigram_dict.keys():
                if smoothing:
                    prob += math.log(float(text.count(word) + 1.0) / (float(unigram_dict[word.split()[0]]) + vocab_length))
                else:
                    prob += math.log(float(text.count(word)) / float(unigram_dict[word.split()[0]]))
            else:
                continue
    else:
        for word in words:
            if word in unigram_dict.keys():
                prob += float(math.log(unigram_dict[word]))
    print(math.log(prob))    
            
    if not perplexity:
        return prob
    else:
        if prob != 0:
            return math.exp(float(1/math.exp(math.log(prob))) ** float(1/len(sentence)))
        else:
            return 0
    
'''
file operations
param: array of file names
'''    
def file_operations(filenames, testfiles, operation):
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
    
    if operation == 1:
        printDictionary(unigram_prob)
        return
    
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
        
    if operation == 2:
        printDictionary(bigram_prob)
        return
    
    if operation == 3:
        printDictionary(addOneSmoothingBigram(unigram_dict, bigram_dict, len_unigram))
        return
    
    tflines = ''
    for tf in testfiles:
         tflines += open(tf, 'r').read()
    print(probfinder(tflines, sentences_with_tag, unigram_dict,True,True,len_unigram,1))
    
    if operation == 6:
        unigram_prob = dict(sorted(unigram_prob.items(), key=itemgetter(1),reverse = True))
        print('Random sentences using Unigram model:')
        for i in range(5):
            print(str(i+1) + " " + randomSentenceGenerator(unigram_prob, sentences_with_tag, len_unigram, bigram_prob,1))
        print('Random sentences using Bigram model:')
        for i in range(5):
            print(str(i+1) + " " + randomSentenceGenerator(unigram_prob, sentences_with_tag, len_unigram, bigram_prob,2))

'''
Author prediction
param:
    filenames: Files used for training and validation
    filenames: Files used for testing
return:
    void
output:
    Prints all predictions for validation set and testing set with line numbers
    and also writes the predictions to result.txt file
'''
def authorPrediction(filenames,test):
    text = ''
    email = dict()
    i = 1
    '''
    Read the training and validation files and construct email dictionary with keys
    being author and values being their email data 
    ''' 
    for filename in filenames:
        f = open(filename, 'r')
        for line in f:
            l1 = line.split()[0]
            l2 = ' '.join(line.split()[1:])
            if l1 in email.keys():
                email[l1] += ' '+l2
            else:
                email[l1] = l2
    #Adjust email data in unigram set
    for k,v in email.items():
        email[k] = set(v.split())
    '''
    Open test files, read data from these files
    and compare which dictionary key has maximum common
    unigrams. The maximum matched unigrams key is author
    predicted by system
    '''
    testfiles = []    
    testfiles.append(filenames[1])
    testfiles.append(test[0])
    i = 1
    fw = open('result.txt','w')
    for filename in testfiles:
        f = open(filename,'r')        
        for line in f:
            l1 = line.split()[0]
            max = 0
            maxk = ''
            for k,v in email.items():
                if len(v.intersection(set(line.split()[1:]))) > max :
                     max = len(v.intersection(set(line.split()[1:])))
                     maxk = k
            fw.write(maxk+'\n')
            print(str(i) + ' ' + maxk)
            i+=1

'''
Main method
param:
    void
return:
    void
'''
def main():
    print('##### NLP Project - 1 #####')
    print('Choose one of the following operations: ')
    print('1 - Unigram Model Generation')
    print('2 - Bigram Model Generation')
    print('3 - Add-one smoothing')
    print('4 - Witten Bell Discounting')
    print('5 - Author prediction')
    print('6 - Random Sentence Generation')
    
    operation = input('Enter input here: ')
    
    if int(operation) == 5:
        authorPrediction(['EnronDataset/train.txt','EnronDataset/validation.txt'],['EnronDataset/test.txt'])
    else:    
        file_operations(['wsj/wsj.train'],['wsj/wsj.test'],int(operation))
                
#Main method is used for starting program                   
main()