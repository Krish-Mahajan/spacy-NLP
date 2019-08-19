'''
Created on Aug 13, 2019

@author: krish.mahajan@ibm.com
'''

import spacy 
import json
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span 
from spacy.tokens import Doc 
from spacy.tokens import Token


class components(object):
    '''
    classdocs
    '''
    
    with open("data/countries.json") as f:
        COUNTRIES = json.loads(f.read(),encoding="utf-8")  
    
            
    with open("data/capitals.json") as f:
        CAPITALS = json.loads(f.read(),encoding="utf-8")  
            
            
    with open("data/bookquotes.json") as f:
         BOOK_DATA = json.loads(f.read())
       
    def __init__(self,nlp):         
        self.add_phrase_matcher(nlp)
        self.add_token_properties() 
        self.add_span_properties()  
        self.add_doc_properties()
        self.add_animal_component_properties(nlp) 
        self.add_countries_component_property(nlp)
        self.add_nlp_components(nlp)

        
        
    def add_phrase_matcher(self,nlp):
        self.matcher = PhraseMatcher(nlp.vocab)
    
    
    
    
    #Define the custom length component
    def length_component(self,doc): 
        #Get the doc's length
        doc_length = len(doc)
        print("This document is {} tokens long".format(doc_length))
        
        #Return the doc
        return doc 
    
    
    def add_animal_component_properties(self,nlp):
        animals = ["Golden Retriever", "cat", "turtle", "Rattus norvegicus"]
        animal_patterns = list(nlp.pipe(animals))
        print("animal_patterns:", animal_patterns)
        self.matcher.add("ANIMAL", None, *animal_patterns) 
        

    #Define the custom animal component 
    def animal_component(self,doc): 
                               
        #Apply the matcher to the doc  
        matches = self.matcher(doc) 
        
        #create a Span for each match and assign the label 'ANIMAL'
        spans = [Span(doc,start ,end , label = "ANIMAL") for match_id , start ,end in matches] 
        print("Spans are:", spans)
        doc.ents = doc.ents + tuple(spans) 
        return doc 
    
    #Define the custom animal component 
    def custom_component(self,doc): 
                               
        #Apply the matcher to the doc  
        matches = self.matcher(doc) 
        
        #create a Span for each match and assign the label 'ANIMAL'
        for match_id , start ,end in matches :
            if nlp.vocab.strings[match_id] == "ANIMAL":
                span = Span(doc,start ,end , label = "ANIMAL") 
                doc.ents = doc.ents + (span,)   
                
            if nlp.vocab.strings[match_id] == "COUNTRY":
                span = Span(doc,start ,end , label = "COUNTRY") 
                doc.ents = doc.ents + span  
        
        return doc
    
        
    
    #Define span properties
    def add_span_properties(self): 
        Span.set_extension('has_color',getter=self.get_has_color) 
        Span.set_extension('to_html',method=self.to_html) 
        Span.set_extension('wikipedia_url',getter=self.get_wikipedia_url) 
        Span.set_extension('capital',getter=self.get_capital) 
        
    
    #Define document properties 
    def add_doc_properties(self):
        Doc.set_extension('has_token',method=self.get_has_token)
        Doc.set_extension('has_number',getter=self.get_has_number)
        Doc.set_extension("author",default=None)
        Doc.set_extension("book",default=None)
    
    
    
    #Define Token properties
    def add_token_properties(self): 
        Token.set_extension('is_color' ,getter=self.get_is_color) 
        Token.set_extension('reversed',getter=self.get_reversed) 
    
    
    
    #Token - color property
    def get_has_color(self,span):
        colors =['red','yellow','blue']
        return any(token.text in colors for token in span)   
    
    #Token- is_color property
    def get_is_color(self,token):
        colors = ['red','yellow','blue']
        return token.text in colors  
    
    #Token - do reverse property
    def get_reversed(self,token):
        return token.text[::-1]
     

    
    
    #Span- HTML property
    def to_html(self,span,tag):
        #wrap the span text in a HTML tag and return it
        return "<{tag}>{text}</{tag}>".format(tag=tag,text=span.text) 
    
    #Span-get wikipedia
    def get_wikipedia_url(self,span):
        if span.label_ in ("PERSON" , "ORG","GPE","LOCATION"):
            entity_text = span.text.replace(" ","-")
            return "https://en.wikipedia.org/w/index.php?search=" + entity_text 
        
    
    #Span-get capital
    def get_capital(self,span):
        return self.CAPITALS.get(span.text)
    
    #Doc - HAS TOKEN property
    def get_has_token(self,doc,token_text):
        in_doc = token_text in [token.text for token in doc]
        return in_doc 
    
    #Doc- HAS No. property
    def get_has_number(self,doc):
        return any(token.like_num for token in doc)
    
    
    
    def add_nlp_components(self,nlp):
        nlp.add_pipe(self.length_component,first=True) 
        #nlp.add_pipe(self.animal_component,after="ner") 
        #nlp.add_pipe(self.countries_component)
        nlp.add_pipe(self.custom_component)
        print(nlp.pipe_names)  

    


    def run_nlp(self,nlp,text):
        doc = nlp(text) 
        return doc   
        
        
        
    def add_countries_component_property(self,nlp): 
        self.matcher.add("COUNTRY", None, *list(nlp.pipe(self.COUNTRIES)))  
        
        
    def countries_component(self,doc): 
        print("here")
        matches = self.matcher(doc)
        spans = [Span(doc,start,end,label="GPE1") for match_id,start,end in matches] 
        doc.ents = doc.ents + tuple(spans)
        return doc
        


if __name__ == '__main__': 
     nlp = spacy.load("en_core_web_sm") 
     cmp = components(nlp)
     text = ["Krishna has a cat and a Golden Retriever.He lives in Czech Republic" , "The sky is blue" ,"I was born in 1991",
             "last album, David Bowie was at the vanguard of contemporary culture." , "Czech Republic may help Slovakia protect its airspace.Krishna has a cat and a Golden Retriever"]
     for data in text: 
        print('Currently processing documet :{}'.format(data))
        doc = cmp.run_nlp(nlp,data) 
        print([(ent.text , ent.label_) for ent in doc.ents]) 
        print(doc[3]._.is_color ,'-',doc[3].text) 
        print(doc[3]._.reversed)
        print(doc[1:4]._.has_color, '-', doc[1:4].text)
        print(doc[0:2]._.has_color, '-', doc[0:2].text)  
        print(doc[0:2]._.to_html("strong"))
        print(doc._.has_token('blue'), '- blue')
        print(doc._.has_token('cloud'), '- cloud')
        print('Document has no. in it :',doc._.has_number)  
        print('Document has following entities: ',doc.ents)
        for ent in doc.ents: 
            print(ent.text , ent.label_, ent._.wikipedia_url , ent._.capital)
        print('-----------------------------------------------') 
        
        
     for doc,context in nlp.pipe(cmp.BOOK_DATA,as_tuples=True):
         doc._.book = context["book"] 
         doc._.author = context["author"] 
        
        #print the text and custom attribute data
         print(doc.text , "\n","- '{}' by {}".format(doc._.book,doc._.author),"\n")
    