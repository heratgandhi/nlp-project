'''
Author: Herat Gandhi
'''
import re
from collections import Counter

'''
file operations
param: array of file names
'''
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
        
        unigram_list = list(Counter(words).items())
        len_unigram = len(unigram_list)
        
        unigram_prob = unigram_list
        unigram_prob = [(unigram[0], unigram[1]/len_unigram) for unigram in unigram_prob]
        
        index_r = 0
        bi_words = words
        while index_r < len(bi_words):
            if index_r + 1 < len(bi_words):
                bi_words[index_r] += " " + bi_words[index_r+1]
            index_r += 1
        
        bigram_list = list(Counter(bi_words).items())
        len_bigram = len(bigram_list)
        
        bigram_prob = bigram_list
        bigram_prob = [(bigram[0], bigram[1] / unigram_list [[x for x, y in enumerate(unigram_list) if y[0] == (bigram[0].split()[0])][0]][1]) for bigram in bigram_prob]
        

def main():
    file_operations(['wsj/wsj.train'])
        
main()