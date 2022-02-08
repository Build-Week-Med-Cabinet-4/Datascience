import os
import sys

# Path restructure for imports
script_dir = os.path.dirname( __file__ )
main_dir = os.path.join( script_dir, '..' )
sys.path.append( main_dir )

from flask import json
import unittest
from strain_api.api import create_strain_api

API = create_strain_api()

class FlaskTestCase(unittest.TestCase):
    '''Class to test the strain_api recommendation route'''
    
    def test_recommend(self):
        '''Test for the recommendation route of app. returns response with strain names'''

        tester = API.test_client(self)

        response = tester.post('/recommend',
            data=json.dumps({"user_input": "indica, lavender, sweet, pepper, relaxed, tingly, happy, creative, aroused, depression, cramps, pain, stress, muscle spasms"}),
            content_type='application/json')

        data = json.loads(response.get_data(as_text=True))

        self.assertEqual({                                              # Json value equal to expected
            "strain_five": "Critical Sensi Star",
            "strain_four": "Blackberry Rhino",
            "strain_one": "Bhang Mr. Nice",
            "strain_three": "Bhang Lavender Kush",
            "strain_two": "Candy Cane"
            }, data)
        self.assertEqual(401, response.status_code)                     # Status code equal to expected
        self.assertEqual('application/json', response.content_type)     # Content_type equal to expected

    def test_content_type(self):
        '''Test to check if the content type checking is functioning'''

        tester = API.test_client(self)

        response = tester.post('/recommend',
            data="indica, lavender, sweet, pepper, relaxed, tingly, happy, creative, aroused, depression, cramps, pain, stress, muscle spasms",     # Data input irrelevant for this call
            content_type='html/text')

        self.assertEqual(401, response.status_code)                         # Status code equal to expected
        self.assertEqual(b'Content-Type not supported!', response.data)     # Content_type error as expected

    def test_data_type(self):
        '''Test to check if non json object error is thrown'''

        tester = API.test_client(self)

        response = tester.post('/recommend',
            data=json.dumps({"positive_effect": "relaxed, tingly, happy, creative, aroused"}),      # Removing user_input key
            content_type='application/json')

        self.assertEqual(401, response.status_code)                                                                                 # Status code equal to expected
        self.assertEqual(b'user_input key is missing from json file or user_input value is not equal to string.', response.data)     # User input error as expected

    def test_data_type_two(self):
        '''Test to check if non json object error is thrown'''

        tester = API.test_client(self)

        response = tester.post('/recommend',
            data=json.dumps({"user_input": ['relaxed', 'tingly', 'happy', 'creative', 'aroused']}),     # Sending as array object to throw error
            content_type='application/json')

        self.assertEqual(401, response.status_code)                                                                                 # Status code equal to expected
        self.assertEqual(b'user_input key is missing from json file or user_input value is not equal to string.', response.data)     # User input error as expected


if __name__ == '__main__':
    unittest.main()