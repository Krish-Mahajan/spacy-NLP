'''
Created on Aug 3, 2019

@author: krish.mahajan@ibm.com
''' 

import spacy

from spacy.tokens import Doc,Span

if __name__ == '__main__':
    #Load the small English model
    nlp = spacy.load('en_core_web_sm')
    
    print('Example 1...\n')
    doc = nlp("She ate the pizza") 
    
    #iterate over the tokens 
    print('{:<10}{:<10}{:<10}{:<10}'.format('TEXT','POS','DEPENDENCY','PARENT'))
    for token in doc:
        #print the text and predicted part of speech 
        print('{:10} {:10} {:10} {:15}'.format(token.text , token.pos_ , token.dep_,token.head.text)) 
     
    print("--------------------------------")    
    
    
    print('Example 2...\n')
    doc = nlp(u"Apple is looking at buying U.K startup for $1 billion") 
    
    span_with_label = Span(doc, 1, 2, label ="GREETING")
    
    
    print('Previous entities :{} '.format(doc.ents))
    doc.ents = doc.ents + (span_with_label,)
    print('New entities after adding custom entities :{}\n'.format(doc.ents))
    
    #iterate over the predicted entities
    print('{:10}{:10}'.format('TEXT','LABEL'))
    for ent in doc.ents :
        #print the entity text and its label
        print('{:10} {:10}'.format(ent.text,ent.label_))  
        
    print("--------------------------------")   
        
    #using matcher
    print('Example 3...\n')
    from spacy.matcher import Matcher
    
    matcher = Matcher(nlp.vocab)
    
    pattern1 = [{'TEXT':'iPhone'},{'TEXT' :'X'}] 
    matcher.add('IPHONE_PATTERN',None,pattern1)
    
    pattern2 = [
    {'IS_DIGIT': True},
    {'LOWER': 'fifa'},
    {'LOWER': 'world'},
    {'LOWER': 'cup'},
    {'IS_PUNCT': True}
    ] 
    
    matcher.add('FIFA_PATTERN',None,pattern2)
 
 
 
    pattern3 = [ {'LEMMA':'love','POS':'VERB'},
                 {'POS': 'NOUN'}
        ]   
    matcher.add('LOVE_PATTERN',None,pattern3) 
    
    
    pattern4 = [
        {'LEMMA':'buy'},
        {'POS':'DET','OP':'?'},
        {'POS':'NOUN'}
        ]
    matcher.add('BUY_PATTERN',None,pattern4) 
    
    data = ['New iPhone X release date leaked','2018 FIFA World Cup: France won!','I loved dogs but now I love cats more.','I bought a smartPhone','I buying apps']
    for text in data:
        doc = nlp(text)    
        matches = matcher(doc)
        for match_id ,start ,end in matches:
            matched_span = doc[start:end]
            print('Following text was matched through custom patterns :{}'.format(matched_span.text ))
        
    