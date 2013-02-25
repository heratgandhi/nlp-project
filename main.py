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

'''
    Print Dictionary
    param:
        my_dictionary: Dictionary to print
'''
def printDictionary(my_dictionary):
    for key,value in my_dictionary.items():
        print(str(key) + ' : ' + str(value))
        
'''
    Witten Bell smoothing 
    Probability mass is shifted around, depending on the context of words
    That is :(N         , T         , null, c          , Z)
'''
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

'''
    Add one smoothing bigrams
    param:
        unigram_dict: Dictionary with unigram and counts
        probability_dict: Dictionary with probabilities
        vocab_length: Length of vocab
    return:
        Dictionary with smoothed probabilities
'''        
def addOneSmoothingBigram(unigram_dict, probability_dict, vocab_length):
    add_one_smooth_bi = dict()
    for key,value in probability_dict.items():
        #Add one in the numerator and add vocab_length in the denominator
        add_one_smooth_bi[key] = float(value + 1.0) / (float(unigram_dict[key.split()[0]]) + vocab_length)
    return add_one_smooth_bi

'''
    Add one smoothing unigrams
    param:
        unigram_dict: Dictionary with unigram and counts
        vocab_length: Distinct no of unigrams
        len_corpus: Length of corpus
    return:
        Dictionary with smoothed probabilities
'''
def addOneSmoothingUnigram(unigram_dict, vocab_length,len_corpus):
    add_one_smooth_uni = dict()
    for key,value in unigram_dict.items():
        add_one_smooth_uni[key] = float(value + 1.0) / (vocab_length+len_corpus)    
    return add_one_smooth_uni

'''
    Random sentence generator
    param:
        unigram_dict: Unigram dictionary with counts
        text: text retrieved from training corpus
        vocab_length: Vocab length
        bigram_prob: Dictionary with bigram probabilities
        Model: 1 for Unigram, 2 for Bigram
'''
def randomSentenceGenerator(unigram_dict,text,vocab_length,bigram_prob,model):
    sentence = ''
    max_prob = unigram_dict[max(unigram_dict, key = lambda x: unigram_dict.get(x) )]
    
    if model == 1:
        '''
            For unigram model, choose random no. between 0 to 1 and get a unigram
            in that range
        '''
        while (not '</s>' in sentence) and (len(sentence) < 30):
            random_p = random.uniform(0.0,max_prob+0.5)
            for key,value in unigram_dict.items():
                if value > random_p - 0.001 and value < random_p + 0.001:
                    sentence += ' ' + key
    else:
        '''
            For bigram model, start with bigram containing <s> and progress
            over with bigram having last word in the sentence 
        '''
        while (not '</s>' in sentence):
            if len(sentence.split()) > 20:
                break
            #Choose random number between 0 and 1
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
    #Remove tags from the text
    sentence = re.sub('<[^<]+>', "", sentence)
    return sentence

'''
Perplexity Calculation
param:
    testfiles: Files used for testing
    text: Text generated from training
    unigram_dict: unigram dictionary with counts
    smoothing: boolean variable whether smoothing should be used or not
    vocab_length: Length of vocabulary
    validationfiles: Validation files used for finding <UNK>
    unigram_prob: Unigram probabilities
return:
    void
output:
    Print unigram and bigram perplexities
Method:
    First find the entropy of the model
    and then use 2 ** Entropy to find perplexity
'''    
def probfinder(testfiles,text,unigram_dict,smoothing,vocab_length,validationfiles,unigram_prob):
    #Read test files
    sentence = ''
    for tf in testfiles:
        #sentence += open(tf, 'r').read()
        with open(tf) as myfile:
            s1 = myfile.readlines(500000)
        for s in s1:
            sentence += s
    #Read validation files
    valid_sentence = ''
    for vf in validationfiles:
        #valid_sentence += open(vf,'r').read()
        with open(vf) as myfile:
            v1 = myfile.readlines(500000)
        for v in v1:
            valid_sentence += v
    #Find UNK's probabilities
    validt_words = list(set(valid_sentence.split()))
    for wd in validt_words:
        if not(wd in unigram_dict.keys()):
            valid_sentence.replace(wd,'<UNK>')
    unk_prob = float(valid_sentence.find('<UNK>')) / len(valid_sentence)
    
    words = list(set(sentence.split()))
    prob = 0
    '''
    Calculate perplexities for unigram model
    If word is found in training then use its probability
    otherwise use UNK's probability
    This for loop calculates entropy of the model
    '''
    for word in words:
        if word in unigram_prob.keys():
            prob += math.log(unigram_prob[word],2) * unigram_prob[word]
        else:
            prob += unk_prob
    
    print('#### Unigram Model Perplexity ####')
    #Find perplexity by 2 ** entropy
    print(2 ** (-1 * prob))
    
    '''
    Calculate perplexities for bigram model
    If word is found in training then use its probability
    otherwise use UNK's probability
    This for loop calculates entropy of the model
    '''
    prob = 0
    index = 0
    while index < len(words)-1:
        words[index] += ' ' + words[index+1]
        index += 1
    words.pop()
    
    for word in words:
        if word.split()[0] in unigram_dict.keys():
            if smoothing:
                prob += math.log(float(text.count(word) + 1.0) / (float(unigram_dict[word.split()[0]]) + vocab_length),2) * (float(text.count(word) + 1.0) / (float(unigram_dict[word.split()[0]]) + vocab_length))
            else:
                prob += math.log(float(text.count(word)) / float(unigram_dict[word.split()[0]])) * float(text.count(word),2) * (float(text.count(word)) / float(unigram_dict[word.split()[0]])) * float(text.count(word))
        else:
            prob += unk_prob
    
    print('#### Bigram Model Perplexity ####')
    #Find perplexity by 2 ** entropy
    print(2 ** (-1 * prob))
    
'''
File operations
param:
    filenames: Files used for training
    validationfiles: Files used for validation
    filenames: Files used for testing
    operation: Operation to be performed
return:
    void
'''    
def file_operations(filenames, validationfiles, testfiles, operation):
    sentences_with_tag = ''
    
    '''
    Read sentences from training file
    '''
    for filename in filenames:
        '''
        If operation is to find perplexity then we just read few lines
        because otherwise the value of perplexity becomes very high.
        '''
        if operation == 7 or 4:
            with open(filename) as myfile:
                lines1 = myfile.readlines(4000)
            lines = ''
            for l in lines1:
                lines += l            
        else:
            lines = open(filename, 'r').read()
        #Remove xml tags from text
        lines = re.sub('<[^<]+>', "", lines)
        #Split lines from the file
        sentences = re.compile(r'(?<=[.!?;])\s*').split(lines)
        #Add sentence start and end markers
        for sentence in sentences:
            sentences_with_tag += ' <s> '+sentence+' </s> '
    #Get all the words         
    words = sentences_with_tag.split()
    #Construct a unigram dictionary
    unigram_dict = dict(Counter(words).items())
    #Find length of unigram dictionary
    len_unigram = len(unigram_dict)
    #Calculate and store probabilities in seperate dictionaries 
    unigram_prob = dict(unigram_dict)
    for key, value in unigram_prob.items():
        unigram_prob[key] = float(value/len_unigram)
    #Calculate unigram probabilities
    if operation == 1:
        print ('#### Unigram Probabilities #####')
        printDictionary(unigram_prob)
        return
    #Construct various bigrams
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
    #Bigram probabilities    
    if operation == 2:
        print ('#### Bigram Probabilities #####')
        printDictionary(bigram_prob)
        return
    #Addone smoothing for bigrams
    if operation == 3:
        print ('#### Add-one smoothing bigrams results #####')
        printDictionary(addOneSmoothingBigram(unigram_dict, bigram_dict, len_unigram))
        return
    #Addone smoothing for unigrams
    if operation == 8:
        print('#### Add-one smoothing unigrams results ####')
        printDictionary(addOneSmoothingUnigram(unigram_dict, len_unigram,len(words)))
        return
    #Perplexity computation
    if operation == 7:
        probfinder(testfiles, sentences_with_tag, unigram_dict,True,len_unigram,validationfiles,unigram_prob)
    #Witten bell smoothing
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
    #Generate random sentences using unigram and bigram models
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
    #Adjust email data in unigram set for each author
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
        print('3 - Add-one smoothing for bigrams')
        print('4 - Witten Bell Discounting')
        print('5 - Author prediction')
        print('6 - Random Sentence Generation')
        print('7 - Measure Perplexity')
        print('8 - Add-one smoothing for unigrams')
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