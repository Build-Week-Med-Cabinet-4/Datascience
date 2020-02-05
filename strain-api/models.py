# Importing needed library
from flask_sqlalchemy import SQLAlchemy
import os
import pickle
import pandas as pd


# Setting global var
DB = SQLAlchemy()

def database_update():

    df = pd.read_csv("https://raw.githubusercontent.com/Build-Week-Med-Cabinet-4/Datascience/master/strain-api/Cannabis_Strains_Features.csv")
    #df = df.set_index('id')
    #df = df.head(50)
    # Saving prediction into database
    for i in df.index:
        data_in = User_input(id=i, name=df['Strain'][i], race=df['Type'][i],
                            rating=df['Rating'][i], effects=df['Effects'][i],
                            flavor=df['Flavor'][i], description=df['Description'][i])
        #import pdb; pdb.set_trace()

        DB.session.add(data_in)
    DB.session.commit()

# User input class sets up database tabel
class User_input(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(200), nullable=False)
    race = DB.Column(DB.String(200), nullable=False)
    rating = DB.Column(DB.Integer, nullable=False)
    effects = DB.Column(DB.String(250), nullable=False)
    flavor = DB.Column(DB.String(100), nullable=False)
    description = DB.Column(DB.String(5000), nullable=False)


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
