# Importing needed library
from flask_sqlalchemy import SQLAlchemy
import os
import pickle
import pandas as pd

# Setting global var
DB = SQLAlchemy()

# User input class sets up database tabel
class User_input(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    prediction = DB.Column(DB.Integer, nullable=False) # Will have ot change once I now the prediction format

    # Returns predictions as string
    def __repr__(self):
        return '{}'.format(self.prediction)


# Predictor class loads in pickled model, predicts recommandations with predict method
class Predictor():
    def __init__(self):
        try:
            print('Loading models from expected local directory')
            self.nn = pickle.load(open('./strain-api/Models/nn.pkl','rb'))
            self.tfidf = pickle.load(open('./strain-api/Models/tfidf.pkl','rb'))
            print('Loaded Successfully')
        except Exception as e:
            print(e)
            print('Trying to load with OS Library')
            self.nn = pickle.load(open(os.getcwd()+'./strain-api/Models/nn.pkl','rb'))
            self.tfidf = pickle.load(open(os.getcwd()+'./strain-api/Models/tfidf.pkl','rb'))
            print('Loaded Successfully')

    # when called predicts recommendations given string input
    def predict(self, input_text, output_size):
        tokens = self.tfidf.transform([input_text]).todense()
        return self.nn.kneighbors(tokens, n_neighbors=output_size)[1][0]
