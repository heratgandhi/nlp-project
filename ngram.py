'''
Author: Herat Gandhi
'''
import re

def dupli(the_list):
    the_m_list = the_list.split()
    count = the_m_list.count
    result = [(item, count(item)) for item in set(the_m_list)]
    return result

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
        print (dupli(sentences_with_tag))
        

def main():
    file_operations(['wsj/wsj.train'])
        
main()