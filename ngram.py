'''
Author: Herat Gandhi
'''
import re
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
            sentences_with_tag += '<s> '+sentence+' </s>'

def main():
    file_operations(['wsj/wsj.test'])
        
main()