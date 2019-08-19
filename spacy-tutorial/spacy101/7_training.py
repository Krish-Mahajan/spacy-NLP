'''
Created on Aug 16, 2019

@author: krish.mahajan@ibm.com
'''

import json
from spacy.matcher import Matcher
from spacy.lang.en import English

if __name__ == '__main__':


    with open("data/iphone.json") as f:
        TEXTS = json.loads(f.read())

    nlp = English()
    matcher = Matcher(nlp.vocab)
    
    # Two tokens whose lowercase forms match 'iphone' and 'x'
    pattern1 = [{"LOWER": "iphone"}, {"LOWER": "x"}]
    
    # Token whose lowercase form matches 'iphone' and an optional digit
    pattern2 = [{"LOWER": "iphone"}, {"IS_DIGIT": True, "OP": "?"}]
    
    # Add patterns to the matcher
    matcher.add("GADGET", None, pattern1, pattern2) 
    
    
    TRAINING_DATA = []

# Create a Doc object for each text in TEXTS
    for doc in nlp.pipe(TEXTS):
        # Match on the doc and create a list of matched spans
        spans = [doc[start:end] for match_id, start, end in matcher(doc)]
        # Get (start character, end character, label) tuples of matches
        entities = [(span.start_char, span.end_char, "GADGET") for span in spans]
        # Format the matches as a (doc.text, entities) tuple
        training_example = (doc.text, {"entities": entities})
        # Append the example to the training data
        TRAINING_DATA.append(training_example)
    
    print(*TRAINING_DATA, sep="\n")