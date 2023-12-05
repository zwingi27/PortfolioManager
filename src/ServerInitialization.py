from components.PackagesGSC import *   
from components.GeneralFunction import *


# this app uses the stylesheet "bootstrap.css" located in the assets folder
app = dash.Dash(__name__, suppress_callback_exceptions=True, title='Finance Portfolio Manager') #title is the title of the Tab in the browser
server = app.server
