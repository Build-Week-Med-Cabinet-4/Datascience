# Importing needed libraries and files
import traceback
import pandas as pd
import numpy as np
from decouple import config
from flask import Flask, request, jsonify
from sklearn.externals import joblib
from .models import DB, User_input, Predictor


# Loading in the trained model pickle file
#lr_model = joblib.load("model.pkl") # Load "model.pkl"
#print ('Model loaded')

lr_model = Predictor()

def create_api():
    '''
    Launches api
    '''

    # configuring flask and SQLAlchemy
    api = Flask(__name__)
    api.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(api)

    @api.route('/')
    def root():
        DB.create_all()
        return 'Startup Test'


    @api.route('/search', methods=['GET'])
    def  search():
        '''
        Overview: takes in prediction id and querys the matching prediction.
        this prevents the prediction step from having to be done more than
        once. If id is not inputed an error will be returned.
        '''

        try:
            id = request.get_json()
            id = id['id']
            result = User_input.query.filter(User_input.id==id).all()
            result = result[0]
            return jsonify({'prediction': result.prediction})

        except:

            # Return tracback response
            print('You must specify the user id')
            return jsonify({'trace': traceback.format_exc()})


    @api.route('/predict', methods=['POST'])
    def predict():
        '''
        Overview: takes in user inputs in json format. converts to string,
        uses trained pickled model to predict recommendations. Returns
        results in json format. Saves predictions with id into database

        '''
        # If trained model loaded
        if lr_model:

            # Attempting to give response
            try:

                # Creating tabel
                DB.create_all()

                # Importing file
                inputs = request.get_json()

                # Breaking down the dictionary
                positive_effect = inputs['positive_effect'][0]
                negative_effect = inputs['negative_effect'][0]
                medical_effect = inputs['negative_effect'][0]
                flavors = inputs['flavor'][0]
                desc = inputs['desc'][0]
                min_rating = inputs['min_rating'][0]
                num_resp = inputs['num_resp'][0]

                # Creating input string, predicting on the string, converting results to int
                df_inputs = str(positive_effect+' '+negative_effect+' '+medical_effect+' '+flavors+' '+desc)
                prediction = lr_model.predict(df_inputs, output_size=1)
                pred = int(prediction)

                # Saving prediction into database
                pred_in = User_input(prediction=pred)
                DB.session.add(pred_in)
                DB.session.commit()

                # Querying prediction, returning result prediction and id in json format
                result = User_input.query.filter(User_input.prediction==pred).all()
                result = result[0]
                return jsonify({'prediction': result.prediction, 'id' : result.id})

            # If error occurs
            except:

                # Return tracback response
                return jsonify({'trace': traceback.format_exc()})

        # Triggered if trained model pickle file is not found
        else:
            print ('Train the model first')
            return ('No model here to use')

    return api
