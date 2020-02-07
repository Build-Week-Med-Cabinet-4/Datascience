import os
import spacy


class Tokenizer__():
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            print(e)
            print('Installing en_core_web_sm')
            os.system('python -m spacy download en_core_web_sm')
            self.nlp = spacy.load("en_core_web_sm")

    def tokenize(self, document):
        doc = self.nlp(document)

        # This one line of code is against PEP 8 guidlines
        # I was too afraid to touch it
        return [token.lemma_.strip() for token in doc if (token.is_stop != True) and (token.is_punct != True)]
