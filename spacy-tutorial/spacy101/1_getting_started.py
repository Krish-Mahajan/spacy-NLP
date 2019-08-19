'''
Created on Aug 3, 2019

@author: krish.mahajan@ibm.com
'''

#Import the English language class 
from spacy.lang.en import English
if __name__ == '__main__':
    
    #1.1
    #create the nlp object    
    nlp = English()    
    #create a processing string of text with the nlp object
    doc = nlp("Hello world!")  
    # Iterate over tokens in a doc
    for token in doc:
        print('Token type is {} and Token data is {}'.format(type(token),token.text))
    
    
    
    #1.3 A slice from the doc is a span object
    span = doc[1:4]
    print('Span type is {} and Span data is {}'.format(type(span),span.text)) 
    
    
    #1.4 Lexical Attributes
    doc = nlp("It costs $5.")
    
    print('Index: ',[token.i for token in doc])
    print('Text: ',[token.text for token in doc])
    print('is_alpha: ',[token.is_alpha for token in doc])
    print('is_punct:' ,[token.is_punct for token in doc])
    print('like num: ',[token.like_num for token in doc])
    