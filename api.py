import os
import pickle
import spacy
import joblib

class Predictor():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        try:
            print('Loading models from expected local directory')
            self.nn = pickle.load(open('./Models/nn.pkl','rb'))
            self.tfidf = pickle.load(open('./Models/tfidf.pkl','rb'))
            print('Loaded Successfully')
        except Exception as e:
            print(e)
            print('Trying to load with OS Library')
            self.nn = pickle.load(open(os.getcwd()+'./Models/nn.pkl','rb'))
            self.tfidf = pickle.load(open(os.getcwd()+'./Models/tfidf.pkl','rb'))
            print('Loaded Successfully')

    def predict(self, input_text, output_size):
        tokens = self.tfidf.transform([input_text]).todense()
        return self.nn.kneighbors(tokens, n_neighbors=output_size)[1][0]
    
class Tokenizer__():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        
    def tokenize(self, document):
        doc = self.nlp(document)

        return [token.lemma_.strip() for token in doc if (token.is_stop != True) and (token.is_punct != True)]
        
    