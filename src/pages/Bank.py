from dash.html.Pre import Pre
from components.packages import *   
from components.GeneralFunction import *
import components.MessageStore as msg
from ServerInitialization import app




#layout of the second page "Data Selection"
layoutDataSelection = html.Div([
    
    # with dcc.Store data can be stored in the browser, for further information see the documentation about dash
    # 'memory': The memory store reverts to the default on every page refresh
    dcc.Store(id='storeUploadedData', storage_type='memory'),                    # store uploaded data from 'Data Selection' slider
    dcc.Store(id='storeFileNames', storage_type='memory'),                       # store the names of the uploaded files as a dictionary: key=index, value = filename
    dcc.Store(id='storeLogMessages', storage_type='memory'),                     # store the log Messages
    dcc.Store(id='storeImagePath', storage_type='memory'),                      # store of the path where the image files from the graphs are stored
    dcc.Store(id='storeDirectoryPath', storage_type='memory'),                 # store of the path variable of the path to the uploaded data files
    dcc.Store(id='storeUnits', storage_type='memory'),                           # stores the features unit information, Dictionary: Key=feature, value=unit
    
    
    dbc.Row([
        dbc.Col([
            html.H2('Bank'),
        ]),
        dbc.Col(),
        dbc.Col(),
    ]),

    html.Div(id='displayErrorDropdown',  style={'textAlign': 'center'}),
    html.Div(id='displayErrorDataSelection',  style={'textAlign': 'center'}),
    html.Div(id='displayAlert',  style={'textAlign': 'center'}),
    html.Div(id='displayClearData', style={'textAlign': 'center'}),])



        