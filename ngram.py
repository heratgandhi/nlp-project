'''
Author: Herat Gandhi
'''
import re
'''
file operations
param: array of file names
'''
def file_operations(filenames):
    '''read file first and get contents'''
    for filename in filenames:
        f = open(filename, 'r')
        lines = '';
        for line in f:
            lines += line
        sentences = re.compile('[.!?]').split(lines)
        print (sentences)

def main():
    file_operations(['wsj/wsj.test','wsj/wsj.train'])
        
main()