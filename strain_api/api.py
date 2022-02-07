import os
import sys

# Path restructure for imports
script_dir = os.path.dirname( __file__ )
main_dir = os.path.join( script_dir, '..' )
sys.path.append( main_dir )

from flask import Flask, request, make_response, jsonify
from strain_api.models import Predictor


def create_strain_api():
    '''Main function storing api variable and routes'''
    
    api = Flask(__name__)
    model = Predictor()     # Initiate recommendation model


    @api.route('/recommend', methods=['POST'])
    def recommend():
        '''Takes in json package containing "user_input" and returns
           a response with content-type json containing five
           recommended medical marijuana strains'''

        # Json content type needed
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.json
            if json['user_input'] and type(json['user_input']) == str:     # Json package contain user_input key and value str

                strain_one, strain_two, strain_three, strain_four, strain_five = model.predict(json['user_input'])      # Recommendation class

                # Response output
                response = make_response(
                        jsonify(
                            {"strain_one": strain_one,
                             "strain_two": strain_two,
                             "strain_three": strain_three,
                             "strain_four": strain_four,
                             "strain_five": strain_five}
                        ),
                        401,
                    )
                response.headers["Content-Type"] = "application/json"
                return response
            else:
                response = make_response(
                    'user_input key is missing from json file or user_input value is not equal to string.', 
                     401,
                )
                response.headers["Content-Type"] = "text/plain"
                return response
        else:
            response = make_response(
                'Content-Type not supported!', 
                401,
                )
            response.headers["Content-Type"] = "text/plain"
            return response

    return api
