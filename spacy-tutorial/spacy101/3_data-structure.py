'''
Created on Aug 5, 2019

@author: krish.mahajan@ibm.com
'''
from spacy.lang.en import English
from spacy.tokens import Doc,Span
if __name__ == '__main__': 
    nlp = English()  
    
    print('Example 1...\n')
    doc = nlp("I love coffee")
    print('hash value of coffee: {}'.format(nlp.vocab.strings['coffee']))
    print('string value of coffee:{}'.format(nlp.vocab.strings[nlp.vocab.strings['coffee']]))   
    print("--------------------------------")   
    
    
    
    print('Example 2...\n')
    doc = nlp("I love coffee")
    print('hash value of coffee:{}'.format(doc.vocab.strings['coffee'])) 
    print("--------------------------------")   
    
    
    print('Example 3...\n')
    doc = nlp("I love coffee")
    lexeme = nlp.vocab['coffee']

# Print the lexical attributes
    print('Context independent lexeme value of coffee: {} {} {}'.format(lexeme.text, lexeme.orth, lexeme.is_alpha)) 
    print("--------------------------------")  
    
    
    print('Example 4...\n')
    words = ['Hello','world' ,'!' ,'INDIA']
    spaces = [True, False,False,True]
    
    # create a doc manually
    doc = Doc(nlp.vocab,words = words, spaces=spaces) 
    
    
    #create a span manually
    span = Span(doc,0,2)
    
    #create a span with a label 
    span_with_label = Span(doc,0,2,label="GREETING") 
    
    #Add span to the doc.ents
    doc.ents = doc.ents + (span_with_label,)  
    
    for ent in doc.ents:
        print('ENTS IN DOC and LABEL :{} {}'.format(ent.text,ent.label_))
    
    