import os
import spacy
import joblib

class Predictor():
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            print(e)
            print('Installing en_core_web_sm')
            os.system('python -m spacy download en_core_web_sm')
            self.nlp = spacy.load("en_core_web_sm")

        try:
            print('Loading models from expected local directory')
            self.nn = joblib.load(open('./Models/nn.pkl','rb'))
            self.tfidf = joblib.load(open('./Models/tfidf.pkl','rb'))
            print('Loaded Successfully')
        except Exception as e:
            print(e)
            print('Trying to load with OS Library')
            self.nn = joblib.load(open(os.getcwd()+'./Models/nn.pkl','rb'))
            self.tfidf = joblib.load(open(os.getcwd()+'./Models/tfidf.pkl','rb'))
            print('Loaded Successfully')

    def predict(self, input_text, output_size):
        tokens = self.tfidf.transform([input_text]).todense()
        return self.nn.kneighbors(tokens, n_neighbors=output_size)[1][0]
    
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

        return [token.lemma_.strip() for token in doc if (token.is_stop != True) and (token.is_punct != True)]
        
    