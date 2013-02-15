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
        words = list(Counter(sentences_with_tag.split()).items())
        print(words)

def main():
    file_operations(['wsj/wsj.train'])
        
main()