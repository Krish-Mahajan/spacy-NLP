'''
Created on Aug 6, 2019

@author: krish.mahajan@ibm.com
'''
import spacy
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher 
from spacy.tokens import Span 

if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')

    print(nlp.pipeline) 
    
    
#define a custom component 
def custom_component(doc):
    # print the doc's length 
    print('Doc Length:' ,len(doc))
    return doc

#Add the component first in the pipeline
nlp.add_pipe(custom_component,first = True)

#print the pipeline component names
print('Pipeline:' , nlp.pipe_names) 
doc = nlp("I love coffee") 

animals = ["Golden Retriever", "cat", "turtle", "Rattus norvegicus"]
animal_patterns = list(nlp.pipe(animals))
print(animal_patterns)
print("animal_patterns:", animal_patterns)
matcher = PhraseMatcher(nlp.vocab)
matcher.add("ANIMAL", None, *animal_patterns)

# Define the custom component
def animal_component(doc):
    # Apply the matcher to the doc
    matches = matcher(doc)
    # Create a Span for each match and assign the label 'ANIMAL'
    spans = [Span(doc, start, end, label="ANIMAL") for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    doc.ents = spans
    return doc


# Add the component to the pipeline after the 'ner' component
nlp.add_pipe(animal_component, after="ner")
print(nlp.pipe_names)

# Process the text and print the text and label for the doc.ents
doc = nlp("I have a cat and a Golden Retriever")
print([(ent.text, ent.label_) for ent in doc.ents])