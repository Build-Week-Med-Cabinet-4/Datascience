# Importing needed library
from flask_sqlalchemy import SQLAlchemy
import os
import pickle
import pandas as pd

# Setting global var
DB = SQLAlchemy()

def database_update():

    df = pd.read_csv("")

    # Saving prediction into database
    data_in = User_input(id=df[0], name=df['Strain'], race=df['Type'],
                         rating=df['Rating'], effects=df['Effects'],
                         flavor=[df['Flavor'], description=df['Description'])

    DB.session.add(data_in)
    DB.session.commit()

# User input class sets up database tabel
class User_input(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(20), nullable=False)
    race = DB.Column(DB.String(20), nullable=False)
    rating = DB.Column(DB.Integer, nullable=False)
    effects = DB.Column(DB.String(250), nullable=False)
    flavor = DB.Column(DB.String(100), nullable=False)
    description = DB.Column(DB.String(1000), nullable=False)


    # Returns predictions as string
    def __repr__(self):
        return '{}'.format(self.id)


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
