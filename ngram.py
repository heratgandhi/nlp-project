'''
Author: Herat Gandhi
'''
import re
from bs4 import BeautifulSoup
'''
file operations
param: array of file names
'''
def file_operations(filenames):
    # process each file individually
    for filename in filenames:
        
        #detect corpus so that information can be used for parsing
        if filename.find('wsj') != -1:
            case = 1
        elif filename.find('set3') != -1:
            case = 2
        elif filename.find('set4') != -1:
            case = 3
        else:
            case = 4    
        
        #Get only text
        if case in [1,2,3]:
            xmldoc = BeautifulSoup(filename)
            if case == 1:
                tagName = 'TEXT'
            elif case == 2:
                tagName = 'DOC'
            elif case == 3:
                tagName = 'DOC'
            itemlist = xmldoc.getElementsByTagName(tagName)
            #print (itemlist[0].value)
        '''
        #open file in read mode
        lines = open(filename, 'r').read()
        sentences = re.compile(r'(?<=[.!?;])\s*').split(lines)
        sentences_with_tag = '';
        for sentence in sentences:
            sentences_with_tag += ' <s> '+sentence+' </s> '
        words = list(set(sentences_with_tag.split()))
        #print(len(words))
        print(words)'''
        

def main():
    file_operations(['wsj/wsj.train'])
        
main()