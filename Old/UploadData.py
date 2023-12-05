from components.PackagesGSC import *   
from components.GeneralFunction import *
from ServerInitialization import app
import components.MessageStore as msg



#layout of the fifth page "Data Storage"
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
                    "Raiffeisen Volskbank: ",
                    dcc.Upload(              # upload files via drag and drop
                        id='uploadDataDragAndDrop',
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
                #dbc.Col([                       # second column
                #    html.Div(id='displayDataFilename'),
                #    html.Div(id='displaySizeDataFrame'),
                #]),
            ])
        ]),
        html.Br(),
        
     #------------------Drag and drop Aktien----------------------------------------------------------------------------------    
        html.Div([
            dbc.Row([ 
                dbc.Col([
                    "Aktien: ",
                    dcc.Upload(              # upload files via drag and drop
                        id='uploadDataDragAndDrop',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files',
                                    style={'textDecoration': 'underline', 'color': 'blue', 'cursor': 'pointer'})
                        ]),
                        style={'width': '80%', 'height': '60px', 'lineHeight': '60px','borderWidth': '1px',
                            'borderStyle': 'dashed','borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '10px'
                        },
                        multiple=True           # Allow multiple files to be uploaded
                    ),
                ]),
                dbc.Col([                       # second column
                    html.Div(id='displayDataFilename'),
                    html.Div(id='displaySizeDataFrame'),
                ]),
            ])
        ]),
        html.Br(),
        
    #--------------------------------------Speicher Button-------------------------------------------------
        html.Div([
            html.Div([
            html.Div(id='displayDatasets', style={'textAlign': 'center'}),               # for error and success messages
            ]),
            dbc.Col([
            
            dbc.Row([ 
                dbc.Col([                                      # button to store the data in a file
                    html.Br(),
                    html.Div(id='displayDataset'),
                ]),
                dbc.Col(

                ),
                dbc.Col(),
            ]),
            ]),
            
            html.Div(id='placeholder'),
        ]),
        html.Br(),
        html.Br(),
        html.Br(),
])



#callback functions for the StoreData page


#callback to show and save the changed Dataset
@app.callback([Output('displayWarningStorage', 'children'), Output('displayDatasets', 'children')],
              [Input('storeUploadedData', 'data'), 
               Input('buttonSaveDataset', 'n_clicks'), Input('dropdownFormat', 'value'),
               Input('inputFilename', 'value'), Input('inputDirectoryPath', 'value'),
               Input('buttonHiddenStoreData', 'n_clicks')])
def SaveDataset(dataUploaded, btnSaveData, fileFormat, fileName, directoryPath, btnHidden):

    if dataUploaded is not None: 
        df = pd.DataFrame.from_dict(dataUploaded)
    else:
        alertError = html.Div([                                        # show error message if there is no dataset to visualize
            html.Br(),
            dbc.Alert([msg.errorNoUploadedData], color="danger")
        ])
        return alertError, None


    ctx = dash.callback_context
    if ctx.triggered:
        buttonId = ctx.triggered[0]['prop_id'].split('.')[0]             # get the id of the button which was triggered
        
        if buttonId == 'buttonSaveDataset'  and directoryPath is not None and dataUploaded is not None: # save data only when fileName, directoryPath and fileFormat are provided
        
            try:                                                         # If no data is uploaded then throw a warning
                if fileName is not None and fileName != "":
                    if directoryPath is not None and directoryPath != "":
                        if fileFormat is not None and fileFormat !="":
                                                                            # Reset the counter of the data frames, since in in 'FeatureEngineering' rows can be dropped
                            df_help1 = pd.DataFrame()
                            indexList = list(pd.unique(df["Index"]))                             # List of indexes of the datafiles
                            for index in indexList:
                                df_help2 = df[df["Index"]==index].drop(columns=["Counter"])      # Delete old Counter
                                df_help2["Counter"] = range(df_help2.shape[0])                   # reset Counter
                                df_help1 = pd.concat([df_help1, df_help2])
                            df = df_help1                                                      


                            if fileFormat == '.csv':                                                 # save data as csv file
                                filePath_help = os.path.join(directoryPath, fileName + fileFormat)   # concatenate the inputs to a complete path, e.g. C:\Users\...\Desktop\Testfile.csv
                                df.to_csv(filePath_help, index=False)                                # save the dataframe as a csv, index=False: the name of the index are not visible in the csv
                                
                                successAlert = html.Div([
                                    dbc.Alert([msg.successStoreDataset], color='success')
                                ])
                                return None, successAlert
                                                                                                    # if semicolon separation is needed, just add: sep=";" to df.to_csv(..., sep=";")
                            elif fileFormat == '.json':                                              # save data as json file
                                filePath_help = os.path.join(directoryPath, fileName + fileFormat)   
                                df.to_json(filePath_help)                                            # save the dataframe as a json
                                
                                successAlert = html.Div([
                                    dbc.Alert([msg.successStoreDataset], color="success")
                                ])
                                return None, successAlert
                        else:
                            alert = html.Div([
                                dbc.Alert([msg.errorFileFormat], color='danger')
                            ])
                            return None, alert
                            
                    else:
                        alert = html.Div([
                                dbc.Alert([msg.errorFilepath], color='danger')
                        ])
                        return None, alert
                        
                else:
                    alert = html.Div([
                        dbc.Alert([msg.errorFilename], color='danger')
                    ])
                    return None, alert
            except:
                alertWarning = html.Div([                                           # show error message if exception occurs when saving data
                    dbc.Alert([msg.error], color="danger")
                ])
                return alertWarning, None
            
        else:
            raise PreventUpdate                

    else:
        raise PreventUpdate                                                                                # prevent page from update when no input has changed
    
    

# callback to create summary
@app.callback(Output('displaySavedMessage', 'children'), 
              [Input('storeUploadedData', 'data'), 
               Input('storeLogMessages', 'data'), Input('inputSummaryName', 'value'), 
               Input('inputDirectoryPathSummary', 'value'), Input('storeFileNames', 'data'), 
               Input('buttonCreateSummary', 'n_clicks'), 
               Input('storeImagePath', 'data'),
               Input('dropdownCustomer','value'), Input('dropdownEmployee','value'),
               Input('inputContactName','value'), Input('inputContactCompany','value'),
               Input('inputContactStreet','value'), Input('inputContactStreetNumber','value'),
               Input('inputContactPostalCode','value'), Input('inputContactCity','value'),
               Input('inputContactEmail','value'), Input('inputContactPhone','value'),
               Input('inputContactCountry','value'), Input('inputContactDepartment','value'),
               Input('confirmContactSaving','submit_n_clicks'), Input('buttonHiddenStoreData', 'n_clicks'),
               Input('dropdownContact','value'), Input('storeUnits','data')]) 
def createDocumentSummary(dataUploaded, logging, summaryName, summaryPath, storedFileNames, btnSummary,
                          imagePath, customerContact, employeeContact, contactName, contactCompany, contactStreet,
                          contactStreetNumber, contactPostalCode, contactCity, contactEmail, contactPhone,
                          contactCountry, contactDepartment, confirmSaving, btnHidden, contactType, unitsDictionary):# btnSaveDetails):

    
    if dataUploaded is not None :                                              # show the uploaded data
        df = pd.DataFrame.from_dict(dataUploaded)

        
        changedId = [p['prop_id'] for p in dash.callback_context.triggered][0]
       
        if 'buttonCreateSummary' in changedId:

            customer = {}               # initial initalization of customer
            employee = {}                # initial initalization of emplyee
            
            
            # if customerContact is None:                            # use input fields for customer information
            #     customer['name'] = contactName if contactName is not None else None
            #     customer['company'] = contactCompany if contactCompany is not None else None
            #     customer['phone'] = contactPhone if contactPhone is not None else None
            #     customer['email'] = contactEmail if contactEmail is not None else None
            #     lst_help = [contactStreet, contactStreetNumber, contactPostalCode, contactCity, customerCountry]
            #     if any(i is None for i in lst_help):
            #         address_help = None
            #     else:
            #         address_help = '%s %s, %s %s (%s) ' %(contactStreet, contactStreetNumber, contactPostalCode, contactCity, contactCountry)
            #     customer['address'] = address_help if address_help is not None else None
            #     customer['department'] = contactDepartment if contactDepartment is not None else None
            
            if customerContact is not None:                         # use saved customer information
                with open(r'./components/ContactStoreCustomer.json','r') as f:
                    dataCustomer = json.load(f) 
                for person in dataCustomer:
                    if person.get('name') == customerContact:
                        customer = person
                        
                
            if employeeContact is not None:                        # use saved employee information
                with open(r'./components/ContactStoreMember.json','r') as f:
                    dataMember = json.load(f)
                for person in dataMember:
                    if person.get('name') == employeeContact:
                        employee = person
                        
                        
            
            GetReport(summaryName, imagePath, df, storedFileNames, logging, employee, customer, unitsDictionary, summaryPath)   # create pdf report with reportlab
            messageSaved = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.successStoreReport], color="success")
                    ])
            return messageSaved
        
        if 'confirmContactSaving' in changedId:
            if contactType is None:
                message = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.missingContactType], color="alert")
                    ])
                return message
            
            
            
            customer = {}
            customer['name'] = contactName if contactName is not None else None
            customer['company'] = contactCompany if contactCompany is not None else None
            customer['phone'] = contactPhone if contactPhone is not None else None
            customer['email'] = contactEmail if contactEmail is not None else None
            lst_help = [contactStreet, contactStreetNumber, contactPostalCode, contactCity, contactCountry]
            if any(i is None for i in lst_help):
                address_help = None
            else:
                address_help = '%s %s, %s %s (%s) ' %(contactStreet, contactStreetNumber, contactPostalCode, contactCity, contactCountry)
            customer['address'] = address_help if address_help is not None else None
            customer['department'] = contactDepartment if contactDepartment is not None else None
            
        
                
            if not all(value is None for key,value in customer.items()):
                with open(r'./components/ContactStore' + contactType + '.json','r') as f:
                    dataCustomer = json.load(f) 
                dataCustomer.append(customer)
                with open(r'./components/ContactStore' + contactType + '.json','w') as f:
                    json.dump(dataCustomer,f)
                message = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.savedContact], color="success")
                    ])
            else:
                message = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.problemContact], color="alert")
                    ])
            return message
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(Output('confirmContactSaving', 'displayed'),
              [Input('buttonSaveCustomerContact', 'n_clicks')])
def ConfirmDialog(btnSave):
    changedId = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'buttonSaveCustomerContact' in changedId:
        return True
    else:
        return False
    
      



# Callback modals

#callback modal for data storage 
@app.callback(
    Output("modalInfoDataStorage", "is_open"),
    [Input("infoButtonDataStorage", "n_clicks"), Input("closeInfoDataStorage", "n_clicks")],
    [State("modalInfoDataStorage", "is_open")],
)
def ToggleModalInfoDataStorage(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen  


#callback modal Information for further Information dropdown
@app.callback(
    Output("modalInfoFurtherInformation", "is_open"),
    [Input("infoButtonFurtherInformation", "n_clicks"), Input("closeInfoFurtherInformation", "n_clicks")],
    [State("modalInfoFurtherInformation", "is_open")],
)
def ToggleModalInfoFurtherInformation(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen  