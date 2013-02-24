'''
Created on Feb 14, 2013

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
        
#Witten Bell smoothing - 
#Probability mass is shifted around, depending on the context of words
#That is :(N         , T         , null, c          , Z)
def wittenBellSmoothingBigram(ngram_list, words, corpus_data, ngram_probabilityList):
    witten_smooth_prob = {}
    for data in corpus_data:
        c = corpus_data[data][3]
        T = corpus_data[data][1]
        Z = corpus_data[data][4]
        N = corpus_data[data][0]
        
        if(c == 0):
            witten_smooth_prob[data] = float(T / float(Z * float(len(ngram_list) + T)))
        else :
            if((N + T) is not 0) : 
                witten_smooth_prob[data] = float(c / float(N + T))
            else :
                #Handle the case when the bigram has just one word in the key
                witten_smooth_prob[data] = ngram_probabilityList[data]
    return witten_smooth_prob        
        
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
        
def probfinder(testfiles,text,unigram_dict,smoothing,vocab_length,validationfiles):
    sentence = ''
    for tf in testfiles:
        sentence += open(tf, 'r').read()
    
    valid_sentence = ''
    for vf in validationfiles:
        valid_sentence += open(vf,'r').read()
    
    validt_words = list(set(valid_sentence.split()))
    for wd in validt_words:
        if not(wd in unigram_dict.keys()):
            valid_sentence.replace(wd,'<UNK>')
    unk_prob = float(valid_sentence.find('<UNK>')) / float(vocab_length)
    
    words = list(set(sentence.split()))
    prob = 0
    
    for word in words:
        if word in unigram_dict.keys():
            prob += float(math.log(unigram_dict[word]))
        else:
            prob += unk_prob
    
    print('#### Unigram Model Perplexity ####')
    print(math.exp( (prob * -1) / len(words) ))
    
    prob = 0
    index = 0
    #words = list(set(words))
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
            prob += unk_prob
    
    print('#### Bigram Model Perplexity ####')
    print(math.exp( (prob * -1) / len(words) ))
    
'''
file operations
param: array of file names
'''    
def file_operations(filenames, validationfiles, testfiles, operation):
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
        print ('#### Unigram Probabilities #####')
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
        print ('#### Bigram Probabilities #####')
        printDictionary(bigram_prob)
        return
    
    if operation == 3:
        print ('#### Add-one smoothing results #####')
        printDictionary(addOneSmoothingBigram(unigram_dict, bigram_dict, len_unigram))
        return
    
    if operation == 7:
        probfinder(testfiles, sentences_with_tag, unigram_dict,True,len_unigram,validationfiles)
    
    if operation == 4:
        list1 = {}
        list_vocab_after = []
        tempWordsList = sentences_with_tag.split()
        #Iterate over all the tokens
        #Pop the last word into a list to keep track of the words after w-1
        for i in range (0, len(words)):
            
            list_vocab_after.append(i + 1)
            poppedWord = tempWordsList.pop()
            list_vocab_after[i] = poppedWord
            
            count_bigramCount_0 = 0
    
            if(tempWordsList.__len__() > 0) :
                for key in bigram_dict:
                    if(key.split()[0] == poppedWord):
                        if(bigram_dict[key] == 0):
                            count_bigramCount_0 = count_bigramCount_0 + 1
                        if(not(key in list1.keys())):
                            #list has (Word_count, VocabCount, null, bigramCount, ZeroCount)
                            #That is :(N         , T         , null, c          , Z)
                            list1[key] = i, Counter(list_vocab_after).items().__len__() - 1, 0 , bigram_dict[key], count_bigramCount_0
        wittenBellDictionary = wittenBellSmoothingBigram(bigram_dict, tempWordsList, list1, bigram_prob)
        print ('#### Witten Bell Discounting results #####')
        printDictionary(wittenBellDictionary)
        return
    
    if operation == 6:
        unigram_prob = dict(sorted(unigram_prob.items(), key=itemgetter(1),reverse = True))
        print('#### Random sentences using Unigram model: ####')
        for i in range(5):
            print(str(i+1) + " " + randomSentenceGenerator(unigram_prob, sentences_with_tag, len_unigram, bigram_prob,1))
        print('#### Random sentences using Bigram model: ####')
        for i in range(5):
            print(str(i+1) + " " + randomSentenceGenerator(unigram_prob, sentences_with_tag, len_unigram, bigram_prob,2))
        return

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
    unigrams. The maximum matched unigrams' key is author
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
    operation = -1
    
    while int(operation) != 0:
        print('')
        print('##### NLP Project - 1 #####')
        print('Choose one of the following operations: ')
        print('1 - Unigram Model Generation')
        print('2 - Bigram Model Generation')
        print('3 - Add-one smoothing')
        print('4 - Witten Bell Discounting')
        print('5 - Author prediction')
        print('6 - Random Sentence Generation')
        print('7 - Measure Perplexity')
        print('0 - Exit')
        print('')
        operation = input('Enter input here: ')
        
        if int(operation) == 5:
            authorPrediction(['EnronDataset/train.txt','EnronDataset/validation.txt'],['EnronDataset/test.txt'])
        elif int(operation) > 0:
            filename = input('Enter training file name(E.g; wsj/wsj.train): ')
            if int(operation) == 7:
                validate_file = input('Enter validation file name(E.g; wsj/wsj.validation): ')
                test_file = input('Enter testing file name(E.g; wsj/wsj.test): ')
                file_operations([filename],[validate_file],[test_file],int(operation))
            else:
                file_operations([filename],[],[],int(operation))
                
#Main method is used for starting program                   
main()