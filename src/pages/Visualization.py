from components.packages import *   
from components.GeneralFunction import *
import components.MessageStore as msg
from ServerInitialization import app


#layout of the third page "Visualization"
layoutVisualization = html.Div([
    
    # 'memory' allows to store larger data than 'session' but data is lost if browser refreshes
    dcc.Store(id='storeUploadedData', storage_type='memory'),                      # store for uploaded data from'Data Selection' slider
    dcc.Store(id='storeFileNames', storage_type='memory'),                         # store for the names of the uploaded files. They are stored in a dictionary
    dcc.Store(id='storeLogMessages', storage_type='memory'),                        # store the log Messages
    dcc.Store(id='storeDirectoryPath', storage_type='memory'),                         # store the directory path of 'Data Seletion' slider         
    dcc.Store(id='storeFilterData', storage_type= 'memory'),                        # store the Data after filter
    dcc.Store(id='storeImagePath', storage_type= 'memory'),                          # store the path of the images
    dcc.Store(id='storeUnits', storage_type='memory'),                           # stores the features unit information, Dictionary: Key=feature, value=unit
    
    
    dbc.Row([
        dbc.Col([
            html.H2('Stocks'),
            ]),
        dbc.Col([
                dbc.Button("i", id="infoButtonVisualization",color="info", className="mr-1", size="sm", n_clicks=0,
                    style={'width': '30px', 'height': '30px', 'borderRadius': '15px',
                        'textAlign': 'center', 'marginBottom': '5px',}),
                dbc.Modal([ 
                    dbc.ModalHeader("Description of visualization slider."),
                    dbc.ModalBody([
                        html.P('In this slide it is possible to create two kinds of profiling reports (Pandas Profiling and SweetVIZ Profiling). '),
                        html.P('In addition, you can filter the data by a feature and by its values.'),
                        html.P('Moreover, it is possible to visualize the previous uploaded data with different plots (scatter plots, line plots, heatmap) '),
                        html.P('It is also possible to interact with the plots and zoom in and out, select a specific area or download the plot as an image file.'),
                    ]),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="closeInfoVisualization", className="ml-auto", n_clicks=0)
                    )
                ],
                id="modalInfoVisualization",
                size="lg",
                is_open=False,
                ),   
            ]),
        dbc.Col(),
    ]),
#------------------------------------------- Error ---------------------------------------------------
    html.Br(),
    html.Div(id='displayErrorLinePlot',  style={'textAlign': 'center'}),
    
    html.Div([
        html.Div(id='displayErrorNoData', style={'textAlign': 'center'}),
    ]),
    

        ])
    
    
    
    #---------------------------previous and next Button--------------------------------------------------------------------------
html.Br(),
html.Div([ 
    html.Div([
        dbc.Button("Previous", size="md", className="mr-1", href="/pages/DataSelection")
    ], style={'textAlign': 'left'}),
    html.Div([
        dbc.Button("Next", size="md", className="mr-1", href="/pages/StoreData")
    ], style={'textAlign': 'right'}),
], style={'columnCount': 2}),


# callback functions of the Visualization page

@app.callback(Output('displayErrorNoData', 'children'),
        [Input('storeUploadedData', 'data'), Input('buttonHiddenPlots', 'n_clicks')])
def ErrorCallback(dataUploaded, btnHidden):
    
    if dataUploaded is None:
        alert = html.Div([
                html.Br(),
                dbc.Alert([msg.errorNoUploadedData], color="danger")
            ])
        return alert
    else:
        return None


# callback options for dropdown for scatter plot, heatmap
@app.callback([Output('dropdownScatter', 'options'), Output('dropdownHeatmap','options'),
                Output('dropdownLinePlot', 'options'), Output('dropdownFilterFeature', 'options')],
              [Input('storeUploadedData', 'data'), Input('storeFilterData', 'data'),
               Input('storeFileNames', 'data'), Input('buttonHiddenPlots', 'n_clicks')])
def DropdownOptions(dataUploaded, dataFilter, filenames, btnHidden):
    
    if dataUploaded is not None:                                             # load dataframe from dictionary if dataset was uploaded
        df = pd.DataFrame.from_dict(dataUploaded)
        if dataFilter is not None and dataFilter != "":
            df = pd.DataFrame.from_dict(dataFilter)                          # if filter was used, use filter data
        df_help, _ = DropColumn(df, ['Index', 'Counter'])                       

        dropdownOptions = [{'label': i, 'value': i}for i in df_help.columns]              # dropdown options of Filter, Scatterplot, Heatmap and Lineplot
       
        filenamesList_help = []                                                               # Show filenames and Index
        for index,name in filenames.items():
            filenamesList_help.append(html.P("File: %s , Index: %s  ; "%(name, index))) 
        filenames = html.H6(filenamesList_help)

        return dropdownOptions, dropdownOptions, dropdownOptions, dropdownOptions
    else:
        raise PreventUpdate    
    
    


@app.callback([Output('storeFilterData', 'data'), Output('displayFilter', 'children')],
             [Input('storeUploadedData', 'data'), Input('dropdownFilterFeature', 'value'),
             Input('inputFilterValue', 'value'), Input('buttonFilterData', 'n_clicks')])    
def FilterData(uploadedData, dropdownFilter, inputFilterValue, btnFilter):
    
    changedId = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'buttonFilterData' in changedId:
        
        if  uploadedData is not None:
            df_help = pd.DataFrame.from_dict(uploadedData)
            if dropdownFilter is not None and inputFilterValue is not None and inputFilterValue != "":
                feature= dropdownFilter                                                  # feature to be filtered 
                featureMin_help = df_help[feature].min()                                 # Minimum of feature
                featureMax_help = df_help[feature].max()                                 # Maximum of feature
                value = inputFilterValue                                                  # value to to filtered
                seperator_help= value.find(',')
                
                
                
                if seperator_help == -1:                                                 # filtering after one feature and one value
                    valueFiltered= int(value)
                    
                    if not valueFiltered > featureMax_help and not valueFiltered < featureMin_help:  # for checking the values to see if they are within the permissible range
                        
                        
                        if valueFiltered in df_help[feature].values:                                 # check if value appears in df
                            dfFiltered= df_help.loc[df_help[feature] == valueFiltered]
                            successAlert = html.Div([
                                dbc.Alert([msg.successFilter], color='success')
                            ]) 
                        else:                                                                        # if values does not appear, make intervall, next larger and smaller value in the df are the boundaries
                            
                            smallerValues = []  # all values that are smaller than the selected one
                            largerValues = []   # all values that are larger than the selected one
                            for i in range(df_help.shape[0]):
                                value_help = df_help[feature].values[i]
                                if value_help < valueFiltered:       # if value is smaller than the selected
                                    smallerValues.append(value_help)
                                if value_help > valueFiltered:       # if value is larger than the selected
                                    largerValues.append(value_help)
                            dfFiltered= df_help.loc[(df_help[feature] >= max(smallerValues)) & (df_help[feature] <= min(largerValues))]   # filter data with the value range [min, max]
                            
                            successAlert = html.Div([
                                dbc.Alert(['Data was filtered. The data frame did not include the selected value. Instead all values between %s and %s were used'%(max(smallerValues), min(largerValues))], color='success')
                            ]) 
                            
                        data = dfFiltered.to_dict('records')
                    
                        return data, successAlert
                    else:
                        alert = html.Div([                                                                                       # error message, if values are not in the range
                            dbc.Alert([msg.ErrorFilterValues2], color='danger')
                        ])
                        return None, alert
                           
                else:
                    valueList_help= value.split(',')                                                                             # filtering after one feature and two values
                    value1 = int(valueList_help[0])
                    value2 = int(valueList_help[1])
                    
                    if not value1 > featureMax_help and not value1 < featureMin_help and not value2 > featureMax_help and not value2 < featureMin_help:  ## for checking the values to see if they are within the permissible range
                        
                        value1Smaller = []
                        value1Larger = []
                        value2Smaller = []
                        value2Larger = []
                        for i in range(df_help.shape[0]):
                            value_help = df_help[feature].values[i]
                            value1Smaller.append(value_help) if value_help < value1 else value1Larger.append(value_help)
                            value2Smaller.append(value_help) if value_help < value2 else value2Larger.append(value_help)
                        
                        if value1 > value2:                                                                                     # check which value is higher
                            if value1 not in df_help[feature].values:
                                value1 = min(value1Larger)    # use the next larger value
                            if value2 not in df_help[feature].values:
                                value2 = max(value2Smaller)   # use the next smaller value
                            
                            dfFiltered= df_help.loc[(df_help[feature] >= value2) & (df_help[feature] <= value1)]
                            data = dfFiltered.to_dict('records')
                            successAlert = html.Div([
                                dbc.Alert(['Data was filtered. Used value range [%s, %s]'%(value2, value1)], color='success')
                            ]) 
                            return data, successAlert
                        elif value1 == value2:                                                                                   # check whether the values are the same
                            alert = html.Div([                                                                                   # error message
                                dbc.Alert([msg.errorFilterValues], color='danger')
                            ])
                            return None, alert
                        else:  # value1 < value2
                            if value2 not in df_help[feature].values:
                                value2 = min(value2Larger)    # use the next larger value
                            if value1 not in df_help[feature].values:
                                value1 = max(value1Smaller)   # use the next smaller value
                            
                            dfFiltered= df_help[(df_help[feature] >= value1) & (df_help[feature] <= value2)]
                            data = dfFiltered.to_dict('records')
                            successAlert = html.Div([
                                dbc.Alert(['Data was filtered. Used value range [%s, %s]'%(value1, value2)], color='success')
                            ])  
                            return data, successAlert
                    else:
                        alert = html.Div([                                                                                       # error message, if values are not in the range
                            dbc.Alert([msg.errorFilterValues2], color='danger')
                        ])
                        return None, alert
                        
            # elif dropdownFilter is not None and (inputFilterValue is None or inputFilterValue == ""):                            # filtering after one feature without values
            #     feature = dropdownFilter
            #     dfFiltered = df_help.sort_values(by=[feature])
            #     data = dfFiltered.to_dict('records')
                
            #     successAlert = html.Div([
            #                 dbc.Alert([msg.successFilter], color='success')
            #             ])
            #     return data, successAlert       
            else:
                alert = html.Div([
                html.Br(),
                dbc.Alert([msg.errorFilter], color="danger")
                ])
                return None, alert
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

   
@app.callback([Output('storeFilterData', 'clear_data'),  Output('displayResetFilter', 'children'),
               Output('inputFilterValue', 'value')],
              [Input('storeFilterData', 'data'), Input('buttonResetFilter', 'n_clicks')])            
def ResetFilter(filterData, btnResetFilter):
    
    changedId = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'buttonResetFilter' in changedId:
        alert = html.Div([
                html.Br(),
                dbc.Alert([msg.successResetFilter], color="success")
                ])
        inputValue= ""
        return True, alert, inputValue
    else:
        raise PreventUpdate

    
            
        
        
@app.callback(Output('displayRangeFeatures', 'children'),
              [Input('storeUploadedData', 'data'),Input('dropdownFilterFeature', 'value')])        
def DisplayFeature(data, dropdownFilterValue):
    
    if dropdownFilterValue is not None:
        df = pd.DataFrame.from_dict(data)
        df_help, _ = DropColumn(df, ['Index', 'Counter'])
        filterValue = dropdownFilterValue
        featureMin = df_help[filterValue].min().round(3)
        featureMax = df_help[filterValue].max().round(3)
        displayInfo = 'Minimum: ', featureMin, ', Maximum: ', featureMax
        return displayInfo
    else:
        raise PreventUpdate
    
# callback to store the image path    
@app.callback(Output('storeImagePath', 'data'),
              [Input('inputImagePath', 'value')])    
def StoreImagePath(imagePath):
    
    if imagePath is not None and imagePath != "":
        return imagePath
    else:
        return None  
               

# callback to draw heatmap, has its own callback to enhance performance of updating the plot
@app.callback([Output('graphHeatmap', 'figure'), Output('displayErrorHeatmap','children')], 
             [Input('storeUploadedData', 'data'), Input('storeFilterData', 'data'), 
              Input('sliderCorrelationHeatmap', 'value'), Input('dropdownHeatmap', 'value'), 
              Input('buttonAllFeaturesHeatmap', 'n_clicks'), Input('buttonExecuteHeatmap', 'n_clicks'), 
              Input('buttonHiddenPlots', 'n_clicks'), Input('storeUnits','data')])
def DrawHeatmap(dataUploaded, dataFiltered, sliderCorrelation, valuesHeatmap, btnAllFeatureHeatmap, btnHeatmap, btnHidden, unitsDictionary):
    
    if dataUploaded is not None:
        if dataFiltered is not None:
            df = pd.DataFrame.from_dict(dataFiltered)
        else:
            df = pd.DataFrame.from_dict(dataUploaded)
            
        for column in df.columns:                                                              # visualize only the features with data type int64 or float64, drop the others from the dataset
            if str(df[column].dtype) != "int64" and str(df[column].dtype) != "float64":
                df.drop([column], axis = 1, inplace = True)

        df, _ = DropColumn(df, ['Index', 'Counter'])
        optionsHeatmap = ['pearson', 'spearman', 'kendall']
        
        ctx = dash.callback_context                                                            # determine which input has fired
        if ctx.triggered:                                                                      # true if one of the Inputs has changed
            buttonId = ctx.triggered[0]['prop_id'].split('.')[0]                               # get the id of the fired input
            
            if buttonId == 'buttonAllFeaturesHeatmap':
                list_help = []
                for column in df.columns:
                    if df[column].isin([0]).sum(axis=0) == df.shape[0]:                        # drop columns where only 0 values are
                        list_help.append(column)
                    if sum(1 for i in df[column] if i != df[column][0]) == 0:                  # drop column which only has one value in each row
                        list_help.append(column)
                        
                if len(list_help) > 0:
                    df = df.drop(columns=list_help)
                
                df = df.dropna(axis=0, how='any')                                             # drop columns if only nan values

                figureHeatmap = PlotHeatmap(df, optionsHeatmap[sliderCorrelation], units=unitsDictionary)           # Heatmap of correlation coefficent
                return figureHeatmap, None                                                    # return the variables to the corresponding outputs
            
            elif buttonId == 'buttonExecuteHeatmap':
                if valuesHeatmap is None:
                    alert = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.errorGraphFeature], color="danger")
                        ])
                    return None, alert
                
                if len(valuesHeatmap) < 2:
                    alert = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.errorGraphFeature], color="danger")
                    ])
                    return None, alert
                
                figureHeatmap = PlotHeatmap(df, optionsHeatmap[sliderCorrelation], valuesHeatmap ,units=unitsDictionary)      # Heatmap of correlation coefficent
                return figureHeatmap, None                                                       # return the variables to the corresponding outputs

            else:
                raise PreventUpdate                                                              # prevent to update the page if no data is uploaded
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
            
@app.callback([Output('displayErrorScatterplot', 'children'), Output('displayErrorLineplot2', 'children'),
               Output('displayErrorHeatmap2', 'children'), Output('displayError3dGraph', 'children'),
               Output('displaySuccessScatterplot', 'children'), Output('displaySuccessLineplot', 'children'),
               Output('displaySuccessHeatmap', 'children'), Output('displaySuccess3dGraph', 'children')],
              [Input('inputImagePath', 'value'), Input('graphScatterplot', 'figure'),
               Input('graphLinePlot', 'figure'), Input('graphHeatmap', 'figure'),
               Input('graph3d', 'figure'),Input('buttonStoreScatter', 'n_clicks'),
               Input('buttonStoreLineplot', 'n_clicks'),Input('buttonStoreHeatmap', 'n_clicks'),
               Input('buttonStore3dGraph', 'n_clicks')])            
def StoreGraphs(inputPathImage, graphScatterplot, graphLineplot, graphHeatmap, graph3d,  btnStoreScatter, btnStoreLineplot, btnStoreHeatmap, btnStore3dGraph ):
    
    pathImage = ChangePath(inputPathImage)
    changedId = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'buttonStoreScatter' in changedId:                                           # Storage of Scatterplot
        if graphScatterplot is not None and graphScatterplot != "":
            
            if inputPathImage is not None and inputPathImage != "":
                nameGraph = 'Scatterplot'
                imageName = StoragenameGraph(nameGraph, pathImage)
                plotly.io.write_image(graphScatterplot, pathImage + '/' + imageName, format = 'jpeg', engine='auto')
                
                successAlert = html.Div([
                        dbc.Alert([msg.successStoreScatterplot], color ='success')
                ])
                return None, None, None, None, successAlert, None, None, None
            else:
                alert = html.Div([
                        dbc.Alert([msg.errorStorePath], color="danger")
                ])
            return alert, None, None, None, None, None, None, None
        else:
            alertMissingFigure = html.Div([
                                dbc.Alert([msg.errorScatterplot], color = "danger") 
            ])
            return alertMissingFigure, None, None, None, None, None, None, None
            
    elif 'buttonStoreLineplot' in changedId:                                            # Storage of Lineplot
        if graphLineplot is not None and graphLineplot != "":
            
            if inputPathImage is not None and inputPathImage != "":
                nameGraph = 'Lineplot'
                imageName = StoragenameGraph(nameGraph, pathImage)                              # create filename of plot     
                plotly.io.write_image(graphLineplot, pathImage + '/' + imageName, format = 'jpeg', engine='auto')
        
                successAlert = html.Div([
                            dbc.Alert([msg.successStoreLineplot], color ='success')
                ])
                return None, None, None, None, None, successAlert, None, None
            else:
                alert = html.Div([
                        dbc.Alert([msg.errorStorePath], color="danger")
                ])
                return None, alert, None, None, None, None, None, None
        else:
            alertMissingFigure = html.Div([
                                 dbc.Alert([msg.errorLineplot], color = "danger") 
            ])
            return None, alertMissingFigure, None, None, None, None, None, None
    
    elif 'buttonStoreHeatmap' in changedId:                                             # Storage of Heatmap
        if graphHeatmap is not None and graphHeatmap != "":
            
            if inputPathImage is not None and inputPathImage != "":
                nameGraph = 'Heatmap'
                imageName = StoragenameGraph(nameGraph, pathImage)                      # create filename of plot
                plotly.io.write_image(graphHeatmap, pathImage + '/' + imageName, format = 'jpeg', engine='auto')
                
                successAlert = html.Div([
                            dbc.Alert([msg.successStoreHeatmap], color ='success')
                ])
                return None, None, None, None, None, None, successAlert, None
            else:
                alert = html.Div([
                        dbc.Alert([msg.errorStorePath], color="danger")
                ])
                return None, None, alert, None, None, None, None, None
        else:
            alertMissingFigure = html.Div([
                                 dbc.Alert([msg.errorHeatmap], color = "danger") 
            ])
            return None, None, alertMissingFigure, None, None, None, None, None
    
    elif 'buttonStore3dGraph' in changedId:                                                    # Storage 3D Graph
        if graph3d is not None or graph3d != "":
            
            if inputPathImage is not None and inputPathImage != "":
                nameGraph = '3D_Graph'
                imageName = StoragenameGraph(nameGraph, pathImage)                              # create filename of plot   
                plotly.io.write_image(graph3d, pathImage + '/' + imageName, format = 'jpeg', engine='auto')
                
                successAlert = html.Div([
                               dbc.Alert([msg.successStore3dGraph], color ='success')
                ])
                return None, None, None, None, None, None, None, successAlert
            else:
                alert = html.Div([
                        dbc.Alert([msg.errorStorePath], color="danger")
                ])
                return None, None, None, alert, None, None, None, None
        else:
            alertMissingFigure = html.Div([
                                 dbc.Alert([msg.error3dGraph], color = "danger") 
            ])
            return None, None, None, alertMissingFigure, None, None, None, None
    else:
        raise PreventUpdate
            
            
        
        

#callback to draw scatter plots
@app.callback([Output('graphScatterplot', 'figure'), Output('displayErrorScatter','children')],
              [Input('storeUploadedData', 'data'), Input('storeFilterData', 'data'),
               Input('dropdownScatter', 'value'), Input('buttonExecuteScatter', 'n_clicks'),
               Input('storeUnits', 'data')])
def DrawScatter(dataUploaded, dataFiltered, valuesScatter, btnScatter, unitsDictionary):
    
    if dataUploaded is not None:                                          # load pandas dataframe from dictionary if dataset was uploaded
        if dataFiltered is not None:
            df = pd.DataFrame.from_dict(dataFiltered)
        else:
            df = pd.DataFrame.from_dict(dataUploaded)
        
        for column in df.columns:                                         # visualize only the features with data type int64 or float64, drop the others from the dataset
            if str(df[column].dtype) != "int64" and str(df[column].dtype) != "float64":
                df.drop([column], axis = 1, inplace = True)

        ctx = dash.callback_context                                       # determine which input has fired
        if ctx.triggered:                                                 # true if one of the Inputs has changed
            buttonId = ctx.triggered[0]['prop_id'].split('.')[0]          # get the id of the fired input
            
            if buttonId == 'buttonExecuteScatter':
                if valuesScatter is None:
                    alert = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.errorGraphFeature], color="danger")
                    ])
                    return None, alert
                
                elif len(valuesScatter) < 2:
                    alert = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.errorGraphFeature], color="danger")
                    ])
                    return None, alert
                
                elif len(valuesScatter) > 5:
                    alert = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.errorScatterFeature], color="danger")
                    ])
                    return None, alert
                
                figureScatterPlot = PlotScatterPlot(df, valuesScatter, unitsDictionary)       # Scatterplot
                return figureScatterPlot, None                         # return the variables to the corresponding outputs

            else:
                raise PreventUpdate                                    # prevent to update the page if no data is uploaded
        else:
            raise PreventUpdate                                        # prevent to update the page if no data is uploaded
    else:
        raise PreventUpdate                                            # prevent to update the page if no data is uploaded
    
        
#callback to draw line plot
@app.callback([Output('graphLinePlot', 'figure'), Output('displayErrorLinePlot', 'children')],
              [Input('storeUploadedData', 'data'), Input('storeFilterData', 'data'),
               Input('dropdownLinePlot', 'value'), Input('sliderFraction', 'value'),
               Input('buttonExecuteLinePlot', 'n_clicks'), Input('inputImagePath', 'value'),
               Input('storeUnits','data')])
def DrawLinePlot(dataUploaded, dataFiltered, dropdownValuesLinePlot, sliderValueFraction, btnLineplot, inputPathImage, unitsDictionary):
    
    if dataUploaded is not None:                                       # load pandas dataframe from dictionary if dataset was uploaded
        if dataFiltered is not None:
            df = pd.DataFrame.from_dict(dataFiltered)
        else:
            df = pd.DataFrame.from_dict(dataUploaded)
        
        for column in df.columns:                                      # visualize only the features with data type int64 or float64, drop the others from the dataset
            if str(df[column].dtype) != "int64" and str(df[column].dtype) != "float64":
                df.drop([column], axis = 1, inplace = True)

        if sliderValueFraction is not None:                            # subset of data used for lineplot, histrogram, distribution plot
            if sliderValueFraction != 0:
                df = ReduceData(df, percent=sliderValueFraction)

        ctx = dash.callback_context                                     # determine which input has fired
        if ctx.triggered:                                               # true if one of the Inputs has changed
            buttonId = ctx.triggered[0]['prop_id'].split('.')[0]        # get the id of the fired input
            
            if buttonId == 'buttonExecuteLinePlot':
                if len(dropdownValuesLinePlot) == 1:
                    figureScatterPlot = PlotLinePlot(df, dropdownValuesLinePlot[0], unitsDictionary)     # Scatterplot
                    return figureScatterPlot, None                                      # return the variables to the corresponding outputs  
                else:
                    alert = html.Div([ 
                        html.Br(),
                        dbc.Alert([msg.errorLineplotFeature], color="danger")
                ])
                    return None, alert
            else:
                raise PreventUpdate                              # prevent to update the page if no data is uploaded
                
        else:
            raise PreventUpdate                                  # prevent to update the page if no data is uploaded
    else:
        raise PreventUpdate                                      # prevent to update the page if no data is uploaded
    
    
    
    
@app.callback(Output('graph3d', 'figure'),
              [Input('storeUploadedData', 'data'), Input('storeFilterData', 'data'),
               Input('buttonAllFeatures3dGraph', 'n_clicks'), Input('storeUnits','data')])    
def Draw3dGraph(dataUploaded, dataFiltered,  btnAllFeatures, unitsDictionary):
    
    if dataUploaded is not None:                                       # load pandas dataframe from dictionary if dataset was uploaded
        if dataFiltered is not None:
            df = pd.DataFrame.from_dict(dataFiltered)
        else:
            df = pd.DataFrame.from_dict(dataUploaded)
                
        for column in df.columns:                                      # visualize only the features with data type int64 or float64, drop the others from the dataset
            if str(df[column].dtype) != "int64" and str(df[column].dtype) != "float64":
                df.drop([column], axis = 1, inplace = True)
                
        ctx = dash.callback_context                                     # determine which input has fired
        if ctx.triggered:                                               # true if one of the Inputs has changed
            buttonId = ctx.triggered[0]['prop_id'].split('.')[0]
            
            if buttonId == 'buttonAllFeatures3dGraph':
                
                if unitsDictionary is not None:
                    for column in list(df.columns):
                        if column in unitsDictionary.keys():
                            df = df.rename(columns={column:column+" [%s]"%(unitsDictionary.get(column))})
                
                df_help, _ = DropColumn(df, ['Index', 'Counter'])
                dfColumns = df_help.columns
                
                figureGraph3d= go.Figure(data= [go.Scatter3d(                       # create a 3D Graph
                                  x = df_help[dfColumns[1]].values,
                                  y= df_help[dfColumns[2]].values,
                                  z= df_help[dfColumns[3]].values,
                                  mode="markers",
                                  marker= dict(
                                      size= 8,
                                      color = df_help[dfColumns[0]],
                                      colorscale = 'Viridis',
                                      opacity = 0.7))])
                figureGraph3d.update_layout(scene = dict(xaxis_title=dfColumns[1], yaxis_title=dfColumns[2], zaxis_title=dfColumns[3]))
                figureGraph3d.show()                                                        # open Graph in extra tab
                
                return figureGraph3d        
            else:
                raise PreventUpdate  
    else:
        raise PreventUpdate       
                



## callback to draw histogram and distribution plot (realtive and absolute)
# @app.callback(Output('graphHistogram', 'figure'), 
#                 [Input('storeUploadedData', 'data'), Input('storeDataAfterFeatureEngineering', 'data'), 
#                 Input('sliderFraction', 'value'), Input('sliderHistogram', 'value'),
#                 Input('buttonHiddenPlots', 'n_clicks')])
# def DrawHistogram(dataUploaded, dataAfterEngineering, sliderValueFraction, sliderValueHistogram, btnHidden):
    
#     if dataUploaded is not None:                                                     # load pandas dataframe from dictionary if dataset was uploaded
#         if dataAfterEngineering is not None:
#             df = pd.DataFrame.from_dict(dataAfterEngineering)
#         else:
#             df = pd.DataFrame.from_dict(dataUploaded)
        
#         for column in df.columns:                                                    # visualize only the features with data type int64 or float64, drop the others from the dataset
#             if str(df[column].dtype) != "int64" and str(df[column].dtype) != "float64":
#                 df.drop([column], axis = 1, inplace = True)

#         if sliderValueFraction is not None:                                          # subset of data used for histrogram, distribution plot
#             if sliderValueFraction != 0:
#                 df = ReduceData(df, percent=sliderValueFraction)

#         df, _ = DropColumn(df, ['Index', 'Counter'])

#         if sliderValueHistogram is not None:
#             if sliderValueHistogram == 0:
#                 figureHistogram = PlotHistogram(df, 'histogram')                            # Histogram
                
#             else: 
#                  figureHistogram = PlotHistogram(df, 'probability density')                 # you can change the type of normalization to: 'percent', 'probability', 'density', 'probability density'

#             return figureHistogram                                                           # return the variables to the corresponding outputs
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate                                                                 # prevent to update the page if no data is uploaded

   

#callback if button SweetzViz Report is pressed
@app.callback(Output('displaySweetviz', 'children'),
              [Input('storeUploadedData', 'data'), Input('buttonSweetviz', 'n_clicks')])
def UpdateSweetviz(dataUploaded, btnSweetviz):
    
    changedId = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'buttonSweetviz' in changedId:                                    # is true wenn the button is clicked
        df_help = pd.DataFrame.from_dict(dataUploaded)
        df_help, _= DropColumn(df_help, ['Index', 'Counter'])
        return SWEETVIZReport(df_help)                                  # the SweetViz Report is stored in the directory of your app
    return None


# #callback to create Pandas Profiling Report, does not work yet
@app.callback(Output('displayPandas', 'children'),
              [Input('storeUploadedData', 'data'), Input('inputDirectoryPathPandas', 'value'),
               State('inputPandaFilename', 'value'), Input("buttonPandasProfiling", 'n_clicks')])
def CreatePandasReport(dataUploaded, directoryPath,reportName, btnPandas):
    
    changedId = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "buttonPandasProfiling" in changedId:
        df_help = pd.DataFrame.from_dict(dataUploaded) 
        df_help, _ = DropColumn(df_help, ['Index', 'Counter'])
        PandasProfileReport(df_help, directoryPath, reportName)
    return None


#

#callback modal Visualization
@app.callback(
    Output("modalInfoVisualization", "is_open"),
    [Input("infoButtonVisualization", "n_clicks"), Input("closeInfoVisualization", "n_clicks")],
    [State("modalInfoVisualization", "is_open")],
)
def ToggleModalInfoVisualization(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen      


#callback modal Scatter
@app.callback(
    Output("modalInfoScatter", "is_open"),
    [Input("infoButtonScatter", "n_clicks"), Input("closeInfoScatter", "n_clicks")],
    [State("modalInfoScatter", "is_open")],
)
def ToggleModalInfoScatter(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen       

#callback modal Heatmap
@app.callback(
    Output("modalInfoHeatmap", "is_open"),
    [Input("infoButtonHeatmap", "n_clicks"), Input("closeInfoHeatmap", "n_clicks")],
    [State("modalInfoHeatmap", "is_open")],
)
def ToggleModalInfoHeatmap(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen     

#callback modal Lineplot
@app.callback(
    Output("modalInfoLinePlot", "is_open"),
    [Input("infoButtonLinePlot", "n_clicks"), Input("closeInfoLinePlot", "n_clicks")],
    [State("modalInfoLinePlot", "is_open")],
)
def ToggleModalInfoLineplot(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen    

# callback modal 3d Graph
@app.callback(
    Output("modalInfo3dGraph", "is_open"),
    [Input("infoButton3dGraph", "n_clicks"), Input("closeInfo3dGraph", "n_clicks")],
    [State("modalInfo3dGraph", "is_open")],
)
def ToggleModalInfo3dGraph(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen   


# callback image path
@app.callback(
    Output("modalInfoImagePath", "is_open"),
    [Input("infoButtonImagePath", "n_clicks"), Input("closeInfoImagePath", "n_clicks")],
    [State("modalInfoImagePath", "is_open")],
)
def ToggleModalInfoImagePath(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen 

# callback filter 
@app.callback(
    Output("modalInfoFilter", "is_open"),
    [Input("infoButtonFilter", "n_clicks"), Input("closeInfoFilter", "n_clicks")],
    [State("modalInfoFilter", "is_open")],
)
def ToggleModalInfoImagePath(info, close, isOpen):
    if info or close:
        return not isOpen
    return isOpen 




