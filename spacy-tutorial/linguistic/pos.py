'''
Created on Aug 3, 2019

@author: krish.mahajan@ibm.com
'''

import spacy


if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
    
    for token in doc:
        print(token.text , token.lemma_)