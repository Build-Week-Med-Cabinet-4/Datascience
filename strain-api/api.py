# Importing needed libraries and files
import traceback
import pandas as pd
import numpy as np
from decouple import config
from flask import Flask, request, jsonify
from sklearn.externals import joblib
from .models import DB, User_input, Predictor, database_update


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
        return 'Start-Up Test'

    @api.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        database_update()
        return 'Reset Database Completed'

    @api.route('/search/<id>', methods=['GET'])
    def search(id=None):
        '''
        Overview: takes in prediction id and querys the matching prediction.
        this prevents the prediction step from having to be done more than
        once. If id is not inputed an error will be returned.
        '''
        id = id
        if id is None:
            # Return tracback response
            print('You must specify the strain id')
            return jsonify({'trace': traceback.format_exc()})

        try:
            result = User_input.query.filter(User_input.id==id).all()
            result = result[0]
            return jsonify({
                                'id': result.id,
                                'name': result.name,
                                'race': result.race,
                                'rating':result.rating,
                                'effects': result.effects,
                                'flavor': result.flavor,
                                'description': result.description
                            })

        except Exception as e:

            return str(e)


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
                try:
                    positive_effect = inputs['positive_effect']
                except:
                    positive_effect = ""
                try:
                    negative_effect = inputs['negative_effect']
                except:
                    negative_effect = ""
                try:
                    medical_effect = inputs['negative_effect']
                except:
                    medical_effect = ""
                try:
                    flavors = inputs['flavor']
                except:
                    flavors = ""
                try:
                    desc = inputs['desc']
                except:
                    desc = ""

                # Creating input string, predicting on the string
                # Converting results to int
                df_inputs = str(positive_effect+' '+negative_effect+' '+medical_effect+' '+flavors+' '+desc)
                prediction = lr_model.predict(df_inputs, output_size=1)
                pred = int(prediction)


                # Querying prediction, returning result prediction and id in json format
                result = User_input.query.filter(User_input.id==pred).all()
                result = result[0]

                return jsonify({
                                'id': result.id,
                                'name': result.name,
                                'race': result.race,
                                'flavor': result.flavor,
                                'positive': result.positive,
                                'negative': result.negative,
                                'medical': result.medical,
                                'rating':result.rating,
                                'description': result.description
                                })


            # If error occurs
            except:

                # Return tracback response
                return jsonify({'trace': traceback.format_exc()})

        # Triggered if trained model pickle file is not found
        else:
            print ('Train the model first')
            return ('No model here to use')

    return api
