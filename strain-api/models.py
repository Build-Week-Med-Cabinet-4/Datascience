# Importing needed libraries
from flask_sqlalchemy import SQLAlchemy
import os
import pickle
import pandas as pd
import spacy
import en_core_web_sm
import joblib

# Setting global var for sqlalchemy
DB = SQLAlchemy()


# Important for interactions with database, as far as wiping it is concerned
def database_update():
    '''
    Overview: used to load in csv and and reset User_input table in database
    is called with special decorator route.
    '''
    url = ("https://raw.githubusercontent.com/Build-Week-Med-" +
           "Cabinet-4/Datascience/master/final_merge3.csv")

    # Reading in csv file from github
    df = pd.read_csv(url)
    # Filling in all nan values
    df = df.fillna(" ")

    # Saving csv data into database, for loop breaks down df row by row
    # slowly adds to database, then once for loop conclution table is commited
    # to the database
    for i in df.index:

        data_in = User_input(id=i, name=df['name'][i],
                             race=df['race'][i],
                             rating=df['Rating'][i],
                             positive=df['positive'][i],
                             negative=df['negative'][i],
                             medical=df['medical'][i],
                             flavor=df['flavors'][i],
                             description=df['Description'][i])

        DB.session.add(data_in)
    DB.session.commit()


# User input class sets up database tabel
class User_input(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(200), nullable=False)
    race = DB.Column(DB.String(200), nullable=False)
    rating = DB.Column(DB.String(200), nullable=False)
    positive = DB.Column(DB.String(250), nullable=False)
    negative = DB.Column(DB.String(250), nullable=False)
    medical = DB.Column(DB.String(250), nullable=False)
    flavor = DB.Column(DB.String(250), nullable=False)
    description = DB.Column(DB.String(5000), nullable=False)


# Predictor class loads in pickled model,
# Predicts recommandations with predict method
class Predictor():
    def __init__(self):
        try:
            self.nlp = en_core_web_sm.load()
        except Exception as e:


            # print('Installing en_core_web_sm')
            os.system('python -m spacy download en_core_web_sm')
            self.nlp = en_core_web_sm.load()

        try:
            # print('Loading models from expected local directory')
            self.nn = joblib.load(open('./strain-api/Models/nn.pkl', 'rb'))
            self.tfidf = joblib.load(open('./strain-api/Models' +
                                          '/tfidf.pkl', 'rb'))
            # print('Loaded Successfully')
        except Exception as e:
            # print(e)
            # print('Trying to load with OS Library')
            self.nn = joblib.load(open(os.getcwd()+'./strain-api/Models' +
                                       '/nn.pkl', 'rb'))
            self.tfidf = joblib.load(open(os.getcwd()+'./strain-api/Models' +
                                          '/tfidf.pkl', 'rb'))
            # print('Loaded Successfully')

    def predict(self, input_text, output_size):
        tokens = self.tfidf.transform([input_text]).todense()
        return self.nn.kneighbors(tokens, n_neighbors=output_size)[1][0]


# Recommender class loads in pickled model, recommend several strain ids
# Currently the model can not be loaded do to the contents of the pickle file
try:
    # print('Loading models from expected local directory')
    loaded_nn = pickle.load(open('./strain-api/Models/top_similar.pkl', 'rb'))
    loaded_tfidf = pickle.load(open('./strain-api/Models/ts_tfidf.pkl', 'rb'))
    # print('Loaded Successfully')
except Exception as e:
    # print(e)
    # print('failed to load')
    pass

def ts_predict(input_index):
    tokens = loaded_tfidf.transform([df.Description[input_index]]).todense()
    return loaded_nn.kneighbors(tokens, n_neighbors=3)[1][0]
