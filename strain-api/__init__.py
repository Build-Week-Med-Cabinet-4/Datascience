from .api import strain_api

# Saving create api func as global API var
API = strain_api()

# Helpful code for development
# set FLASK_ENV=development
# set FLASK_APP=strain-api:API
# import pdb; pdb.set_trace()
