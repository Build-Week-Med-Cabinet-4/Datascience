import os
import sys

# Path restructure for imports
script_dir = os.path.dirname( __file__ )
main_dir = os.path.join( script_dir, '..' )
sys.path.append( main_dir )

import json
import pickle
import pandas as pd

class Predictor():
    ''' Class for recommending medical marijuana strains given "user_input".
    
    Attributes:
        feature_dict (dict): contains boolean values for features to be sent to model
        strain_data (DataFrame): contains strain data
        nn (pkl): sklearn Nearest Neighbor recommendation model
        '''

    feature_dict = json.load(open('assets/data/feature_dict.json'))
    strain_data = pd.read_csv('assets/data/strain_data.csv')

    def __init__(self):
        ''' The constructor for Predictor class.
        
            Parameters:
                nn (pkl): sklearn Nearest Neighbor recommendation model'''

        self.nn = pickle.load(open('assets/models/nn_model.pkl', 'rb'))     # Load in the picked nn model
        
    def predict(self, input_text):
        input_text = input_text.split(', ')                         # Formating input text

        for feature in input_text:                                  # Populating boolean table
            self.feature_dict[feature] = 1

        model_input = list(self.feature_dict.values())              # Preping final model input

        _, recommends = self.nn.kneighbors([model_input])           # Preforming model recommendation, returns id values

        # Quarrying the strain names from starin dataset using recommened ids
        strain_one = self.strain_data.values[recommends[0][0]][0]
        strain_two = self.strain_data.values[recommends[0][1]][0] 
        strain_three = self.strain_data.values[recommends[0][2]][0] 
        strain_four = self.strain_data.values[recommends[0][3]][0] 
        strain_five = self.strain_data.values[recommends[0][4]][0] 

        return strain_one, strain_two, strain_three, strain_four, strain_five
