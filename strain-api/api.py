# Importing needed libraries and files
from os import getenv

ELEPHANTSQL_DATABASE = getenv('ELEPHANTSQL_DATABASE')
ELEPHANTSQL_USERNAME = getenv('ELEPHANTSQL_USERNAME')
ELEPHANTSQL_PASSWORD = getenv('ELEPHANTSQL_PASSWORD')
ELEPHANTSQL_HOST = getenv('ELEPHANTSQL_HOST')


import traceback
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from sklearn.externals import joblib
from .models import DB, User_input, database_update, Predictor, li_recommend


# Creating a function for launching api
def create_api():
    '''
    Launches api
    '''
    # Configuring flask and SQLAlchemy
    api = Flask(__name__)
    api.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(api)

    # Just the base route currently has no functionallity
    @api.route('/')
    def root():
        return 'Start-Up Success'

    # Special route to load in and reset the database if need be
    @api.route('/reset')
    def reset():
        '''
        Overview: drops table in database, then creats fresh table
        database_update function is called to load in any updated data
        to the database.
        '''
        DB.drop_all()
        DB.create_all()
        database_update()
        return 'Reset Database Completed'

    # GET request for searching database given id
    @api.route('/search/<id>', methods=['GET'])
    def search(id=None):
        '''
        Overview: takes in prediction id and querys the matching prediction.
        this prevents the prediction step from having to be done more than
        once. If id is not inputed an error will be returned.
        '''
        # Setting id to id
        id = id

        # If no id input
        if id is None:

            # Return meta response
            response = {"id": id, "prediction": "no prediction" +
                        " returned given id status None"}
            return create_json(201, "An id was not specified," +
                               " must include id input. valid" +
                               " call example: https://med-ca" +
                               "binet-4-api.herokuapp.com/se" +
                               "arch/641", response)

        # Attempt to query database info given id
        try:
            result = User_input.query.filter(User_input.id == id).all()
            result = result[0]
            return jsonify({
                            'id': result.id,
                            'name': result.name,
                            'race': result.race,
                            'flavor': result.flavor,
                            'positive': result.positive,
                            'negative': result.negative,
                            'medical': result.medical,
                            'rating': result.rating,
                            'description': result.description
                            })

        # If query failed print response
        except:

            response = {"id": id, "prediction": "no prediction" +
                        " returned given invalid input"}
            return create_json(200, "GET input must be a valid strain id," +
                               " valid ids are ints range 0-3018", response)

    # A GET request to recommend strains based on similarity to strain input
    @api.route('/recommend/<id>', methods=['GET'])
    def recommend(id=None):
        '''
        Overview: Warning currently not running due to a broken pkl file!!!
        When function a GET request can be called with a strain id input that
        is sent to a predictve model that matches similar starin ids. The
        call then outputs recommendations in json format
        '''
        # Setting id to id
        id = id

        # If no id input
        if id is None:

            # Return meta response
            response = {"id": id, "prediction": "no prediction" +
                        " returned given id status None"}
            return create_json(201, "An id was not specified," +
                               " must include id input. valid" +
                               " call example: https://med-ca" +
                               "binet-4-api.herokuapp.com/se" +
                               "arch/641", response)

        # If trained model loaded
        if recommend_model:

            # Attempting to give response
            try:
                # Creating tabel
                DB.create_all()

                # Creating input id in form int, predicting on the id
                # Returns list of recommendatons
                id_input = int(id)
                prediction = ts_predict(input_index=id_input)

                # For consistency saving prediction to pred, creating empt list
                pred = prediction
                holder_list = []

                # For loop to query data based on predictions given above
                for i in pred:
                    # Querying prediction, appending prediction to list
                    result = User_input.query.filter(User_input.id ==
                                                     pred).all()
                    result = result[0]
                    holder_list.append(result)

                # Breaking apart holder_list and sending lists of info back to
                # user. Results are returned in json format in a list
                # Currently only returns three recommendations.
                return jsonify({
                                'id': [holder_list[0].id,
                                       holder_list[1].id,
                                       holder_list[2].id],

                                'name': [holder_list[0].name,
                                         holder_list[1].name,
                                         holder_list[2].name],

                                'race': [holder_list[0].race,
                                         holder_list[1].race,
                                         holder_list[2].race],

                                'flavor': [holder_list[0].flavor,
                                           holder_list[1].flavor,
                                           holder_list[2].flavor],

                                'positive': [holder_list[0].positive,
                                             holder_list[1].positive,
                                             holder_list[2].positive],

                                'negative': [holder_list[0].negative,
                                             holder_list[1].negative,
                                             holder_list[2].negative],

                                'medical': [holder_list[0].medical,
                                            holder_list[1].medical,
                                            holder_list[2].medical],

                                'rating': [holder_list[0].rating,
                                           holder_list[1].rating,
                                           holder_list[2].rating],

                                'description': [holder_list[0].description,
                                                holder_list[1].description,
                                                holder_list[2].description]
                                })

            # If error occurs
            except:

                response = {"id": id, "prediction": "no prediction" +
                            " returned given invalid input"}
                return create_json(200, "GET input must be a valid" +
                                   " strain id, valid ids are ints" +
                                   "range 0-2825", response)

        # Triggered if trained model pickle file is not found
        else:

            return ('Failed to load predictive model files, chec' +
                    'k if api is currently live')

    # POST request to make predictions given user inputs
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

                # Breaking down the dictionary, checking for all inputs
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

            except:

                response = {"id": "Error", "prediction": "Prediction" +
                            " not recommended given invalid json input"}
                return create_json(202, "Must provid valid json inpu" +
                                   "t. please refer to API document" +
                                   "ation", response)

            try:

                # Creating input string, predicting on the string
                # Converting results to int
                df_inputs = str(positive_effect + ' ' +
                                negative_effect + ' ' +
                                medical_effect + ' ' +
                                flavors + ' ' +
                                desc)
                prediction = lr_model.predict(df_inputs, output_size=1)
                pred = int(prediction)

                # Model predicts from 0 to 3018 ids. but database only houses 0
                # to 2825 this statement stops api from breaking.
                # problem will be resolved in future
                if pred > 2825:
                    pred = 2000

                # Querying prediction
                # Returning result prediction and id in json format
                result = User_input.query.filter(User_input.id == pred).all()
                result = result[0]

                return jsonify({
                                'id': result.id,
                                'name': result.name,
                                'race': result.race,
                                'flavor': result.flavor,
                                'positive': result.positive,
                                'negative': result.negative,
                                'medical': result.medical,
                                'rating': result.rating,
                                'description': result.description
                                })

            # If error occurs
            except:

                response = {"id": "Error", "prediction": "Predic" +
                            "tion not recommended, predictive m" +
                            "odel/ query error"}
                return create_json(203, "Unable to make predicti" +
                                   "on or connect to database, " +
                                   " please check if queried dat" +
                                   "abase is live", response)

        # Triggered if trained model pickle file is not found
        else:

            return ('Failed to load predictive model files, chec' +
                    'k if api is currently live')

    return api


# Error code function called when certian errors occur
def create_json(code, description, dictionary=None):
    temp = {
        "meta": {
            "code": code,
            "description": description
        }
    }
    if dictionary is not None:
        temp['response'] = dictionary
    return temp
