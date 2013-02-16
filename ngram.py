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
        index_r = 0
        bi_words = []
        while index_r < len(words):
            if index_r + 1 < len(words):
                bi_words.append(words[index_r] + " " + words[index_r+1])
                index_r += 1
        bigram_list = list(Counter(bi_words).items())

def main():
    file_operations(['wsj/wsj.train'])
        
main()