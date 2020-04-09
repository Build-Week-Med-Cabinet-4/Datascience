import os
import spacy
import joblib

class Predictor():
    def __init__(self):
        print('Loading models from expected local directory')
        self.nn = joblib.load(open('./strain-api/Models/nn.pkl','rb'))
        self.tfidf = joblib.load(open('./strain-api/Models/tfidf.pkl','rb'))
        print('Loaded Successfully')

    def predict(self, input_text, output_size):
        tokens = self.tfidf.transform([input_text]).todense()
        return self.nn.kneighbors(tokens, n_neighbors=output_size)[1][0]
    

        
    