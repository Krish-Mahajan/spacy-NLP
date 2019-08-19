'''
Created on Aug 5, 2019

@author: krish.mahajan@ibm.com
'''
import spacy 
from spacy.lang.en import English
from spacy.tokens import Doc,Span
if __name__ == '__main__':
   
    nlp = English() 
    
    # Load a larger model with vectors
    nlp = spacy.load('en_core_web_md')

    # Compare two documents
    doc1 = nlp("I like fast food")
    doc2 = nlp("I like pizza")
    print(doc1.similarity(doc2)) 
    
    
    doc = nlp("I like pizza")
    token = nlp("soap")[0]

    print(doc.similarity(token)) 
    
    span = nlp("I like pizza and pasta")[2:5]
    doc = nlp("McDonalds sells burgers")

    print(span.similarity(doc)) 
    
    
    # Load a larger model with vectors
    nlp = spacy.load('en_core_web_md')
    
    doc = nlp("I have a banana")
    # Access the vector via the token.vector attribute
    print(doc.vector)