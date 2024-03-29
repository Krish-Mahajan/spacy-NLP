'''
Created on Aug 16, 2019

@author: krish.mahajan@ibm.com
'''

import spacy


if __name__ == '__main__':
    nlp = spacy.load("en_core_web_sm")
    text = (
    "Chick-fil-A is an American fast food restaurant chain headquartered in "
    "the city of College Park, Georgia, specializing in chicken sandwiches."
)

# Disable the tagger and parser
    with nlp.disable_pipes("tagger", "parser"):
        # Process the text
        doc = nlp(text)
        # Print the entities in the doc
        print(doc.ents)