# Importing needed libraries and files
import traceback
import pandas as pd
import numpy as np
from decouple import config
from flask import Flask, request, jsonify
from sklearn.externals import joblib
from .models import DB, User_input, database_update, ts_predict, Predictor

# Calling Predictor class
#lr_model = Predictor()


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

            # Return tracback respons
            print('You must specify the strain id')
            return jsonify({'trace': traceback.format_exc()})

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
        except Exception as e:

            return str(e)

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
            # Return tracback respons
            print('You must specify the strain id')
            return jsonify({'trace': traceback.format_exc()})

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
            except Exception as e:

                return str(e)

        # Triggered if trained model pickle file is not found
        else:
            print ('Train the model first')
            return ('No model here to use')

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

                # Creating input string, predicting on the string
                # Converting results to int
                df_inputs = str(positive_effect + ' ' +
                                negative_effect + ' ' +
                                medical_effect + ' ' +
                                flavors + ' ' +
                                desc)
                prediction = lr_model.predict(df_inputs, output_size=1)
                pred = int(prediction)

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
            except Exception as e:

                return str(e)

        # Triggered if trained model pickle file is not found
        else:
            print ('Train the model first')
            return ('No model here to use')

    return api
