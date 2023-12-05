from components.PackagesGSC import *   
from components.GeneralFunction import *
from ServerInitialization import app

APP_LOGO = "../assets/Finanzguru2.png"                                                                        # constant for the path of the App Logo

#layout of the first page "Start"
layoutStart = html.Div([

    html.H1('Finance Portfolio Manager', style={'textAlign': 'center'}),
    html.Br(),
    html.Div([                                                                                              # display the Grenzebach Logo
        html.Img(src=APP_LOGO, style={'width': '426px', 'height': '206px'})  
    ], style={'textAlign': 'center'}),
    html.Br(),
    html.Div([                                                                                              # start button to continue
        dbc.Button("Bank", size="md", color="info", className="mr-1", href="/pages/Bank"),
        dbc.Button("Stocks", size="md", color="info", className="mr-1", href="/pages/Stocks"),
        dbc.Button("Upload Data", size="md", color="info", className="mr-1", href="/pages/UploadData"),
                ],style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(), 
])