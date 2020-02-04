# Importing from api.py file
from .api import create_api

# Saving create api func as global API var
API = create_api()


#set FLASK_APP=strain-api:API
#import pdb; pdb.set_trace()
