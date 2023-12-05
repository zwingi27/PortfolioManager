from components.packages import *   
from ServerInitialization import app
import components.MessageStore as msg
from classes.databaseClass import PostgressHandler


dataLoader = DataUploader()
layoutStoreData = html.Div([
    
    # 'memory' allows to store larger data than 'session' but data is lost if browser refreshes
    dcc.Store(id='storeUploadedData', storage_type='memory'),                 # store of the uploaded data form the 'DataSelection' slider
    dcc.Store(id='storeLogMessages', storage_type='memory'),                  # store the log Messages
    dcc.Store(id='storeFileNames', storage_type='memory'),                    # store the names of the uploaded files
    dcc.Store(id='storeImagePath', storage_type='memory'),                    # store of the path where the image files from the graphs are stored
    dcc.Store(id='storeDirectoryPath', storage_type='memory'),                # store of the path variable of the path to the uploaded data files
    dcc.Store(id='storeUnits', storage_type='memory'),                           # stores the features unit information, Dictionary: Key=feature, value=unit
    
    dbc.Row([
        dbc.Col([
            html.H2('Upload Data'),
            ]),
        dbc.Col(),
    ]),

    
    html.Div([
        html.Div(id='displayWarningStorage', style={'textAlign': 'center'}),       # the warning message from the callback gets visualized at this position
    ], style={'textAlign': 'center'}),

    html.Br(),

    #-------------------------Hidden Button----------------------------------------------------------------
    html.Div([                                                                     # button is necessary to fire the callback, button is not visualized on the page
        dbc.Button("updateStoreData", id="buttonHiddenStoreData", color="primary", className="mr-1", size="md", n_clicks=0),
    ], hidden='hidden'),

    
    #------------------Drag and drop Raiffeisen----------------------------------------------------------------------------------    
        html.Div([
            dbc.Row([ 
                dbc.Col([
                    "Raiffeisen Volksbank: ",
                    dcc.Upload(              # upload files via drag and drop
                        id='RaibaUploadDataDragAndDrop',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files',
                                    style={'textDecoration': 'underline', 'color': 'blue', 'cursor': 'pointer'})
                        ]),
                        style={'width': '80%', 'height': '60px', 'lineHeight': '60px','borderWidth': '1px',
                            'borderStyle': 'dashed','borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '10px'
                        },
                        multiple=False          # Allow multiple files to be uploaded
                    ),
                ]),
            ])
        ]),
        html.Br(),
        
     #------------------Drag and drop Aktien----------------------------------------------------------------------------------    
        html.Div([
            dbc.Row([ 
                dbc.Col([
                    "Aktien: ",
                    dcc.Upload(              # upload files via drag and drop
                        id='AktienUploadDataDragAndDrop',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files',
                                    style={'textDecoration': 'underline', 'color': 'blue', 'cursor': 'pointer'})
                        ]),
                        style={'width': '80%', 'height': '60px', 'lineHeight': '60px','borderWidth': '1px',
                            'borderStyle': 'dashed','borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '10px'
                        },
                        multiple=False          # Allow multiple files to be uploaded
                    ),
                ]),
            ])
        ]),
        html.Br(),

    #------------------Table of Uploaded Data----------------------------------------------------------------------------------    
    #html.Div(children="Current Data Frame"),
    #dash_table.DataTable(data=dataLoader.df.to_dict('records'),page_size=10)
    html.Div([
        dash_table.DataTable(
            id='my-datatable',
            columns = [{'name': col, 'id': col} for col in dataLoader.df.columns] if dataLoader.df is not None else None,
            data=dataLoader.df.to_dict('records') if dataLoader.df is not None else None,
            page_size=10
        ),
])

])


@app.callback(
    [ 
               Output('RaibaUploadDataDragAndDrop', 'contents'), 
               Output('displayWarningStorage', 'children'), # To display a success or error message
               Output('my-datatable', 'data'),
    ],
    [          Input('RaibaUploadDataDragAndDrop', 'contents'),
               Input('RaibaUploadDataDragAndDrop', 'filename'),
    ]
)
def upload_data_callback(contents, filename):
    if contents is not None:
        # Check if the file is a CSV file
        if 'csv' in filename.lower():
            try:
                dataLoader = DataUploader()
                dataLoader.df = None
                dataLoader.parseData(contents,filename)
                
                success_message = f"File '{filename}' uploaded successfully!"
                return dash.no_update, success_message, dataLoader.df.to_dict('records')
            except Exception as e:
                # Handle any errors that may occur during file processing
                error_message = f"Error: {str(e)}"
                return dash.no_update, error_message,None          
        else:
            # Handle the case when the selected file is not a CSV file
            return dash.no_update, "Error: Please upload a CSV file.",None
    else:
        # Handle the case when no file is selected
        return dash.no_update, "No file selected.", None
        

