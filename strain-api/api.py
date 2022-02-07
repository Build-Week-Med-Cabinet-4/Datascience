from flask import Flask, request, make_response, jsonify
from functools import wraps

def strain_api():
    api = Flask(__name__)

    global current_user

    def auth_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if auth and auth.username == 'username1' and auth.password == 'password':
                global current_user
                current_user = auth.username
                return f(*args, **kwargs)

            return make_response('Could not verify login information', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
        
        return decorated
        
    @api.route('/login')
    @auth_required
    def login():
        response = make_response(
                jsonify(
                    {"token": '',   
                     "message": 'successful login'}
                ),
                401,
            )
        response.headers["Content-Type"] = "application/json"
        return response

    @api.route('/signup', methods=['POST'])
    def signup():
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.json
            if json['username'] and json['password'] and json['fullname']:
                # Add to database
                response = make_response(
                jsonify(
                    {"token": '',   
                     "message": 'successful login'}
                    ),
                401,
                )
                response.headers["Content-Type"] = "application/json"
                return response
            else:
                return 'Username, password, or fullname key is missing from json file'
        else:
            return 'Content-Type not supported!'
    
    @api.route('/dashboard')
    @auth_required
    def dashboard():
        # Get saved strain for current user
        response = make_response(
                jsonify(
                    {"saved_length": 3,
                     "saved_strains": 'name_one, name_two, name three',  
                     "message": 'successful login'}
                ),
                401,
            )
        response.headers["Content-Type"] = "application/json"
        return response
    
    @api.route('/savestrain')
    @auth_required
    def savestrain():
        # save strain to current user database
        response = make_response(
        jsonify(
            {"message": 'strain saved'}
            ),
        401,
        )
        response.headers["Content-Type"] = "application/json"
        return response


    @api.route('/recommend')
    @auth_required
    def recommend():
        response = make_response(
                jsonify(
                    {"strain_one": 'name_one',
                     "strain_two": "name_two",
                     "strain_three": "name_three",
                     "strain_four": "name_four",
                     "strain_five": "name_five",   
                     "message": 'successful login'}
                ),
                401,
            )
        response.headers["Content-Type"] = "application/json"
        return response

    return api
