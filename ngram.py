'''
Author: Herat Gandhi
'''
import re
from collections import Counter

'''
file operations
param: list of file names
'''
def file_operations(filenames):
    for filename in filenames:
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
        unigram_dict = {key: value for (key, value) in unigram_list}
        bigram_prob = [(bigram[0], bigram[1] / unigram_dict [bigram[0].split()[0]]) for bigram in bigram_prob]
        
        print(bigram_prob)
def main():
    file_operations(['small.txt'])
        
main()