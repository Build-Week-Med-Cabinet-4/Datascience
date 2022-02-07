import os
import sys

# Path restructure for imports
script_dir = os.path.dirname( __file__ )
main_dir = os.path.join( script_dir, '..' )
sys.path.append( main_dir )

from strain_api.api import create_strain_api

API = create_strain_api()   # Initializing API


# Helpful code for development
# set FLASK_ENV=development
# set FLASK_APP=strain_api:API
# import pdb; pdb.set_trace()
