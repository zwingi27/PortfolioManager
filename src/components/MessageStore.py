##################### Data Selection ###########################
errorProcessing = 'There was an error processing this file.'    # in function ParseData
errorPath = 'Invalid path input. Please check if the path is correct.'  # in function: DropdownSelectFile
errorFilePath = 'Please check that you have selected the path and the file.' # in function: UpdateTable (buttonLoadFiles)
successClearData = 'Data was removed.'  # in function: UpdateTable (buttonClearData)
errorNoData = 'No data uploaded! Please upload Dataset first' # in function: previewOfData
wrongDataType = 'Only .txt files are allowed.'

wrongFileTypeUnits = 'Only JSON files are allowed.'
successUnits = 'Successfully loaded the units.'
missingUnits = 'Please check if both input fields (feature name and unit) are filled.'
missingFileType = 'Please selected the file filter type in the provided dropdown menue first.'


#################### Visualization ##############################
errorNoUploadedData = 'No data uploaded. Please upload data first on the "Data Selection" page.'    # in function: ErrorCallback, SavaDataset (slide: DataStorage)
errorFilterValues = 'Filter values must be different!'  # in function: FilterData
errorFilterValues2 = 'The filter values entered are not within the permissible range.' # in function: FilterData 
successFilter = 'Data was filtered.'    # in function: FilterData
errorFilter = 'Please check whether a feature and a value is selected.' # in function: FilterData
successResetFilter = 'Filter was reset.'    # in function: ResetFilter
errorGraphFeature = 'Please select at least 2 features' # in function: DrawHeatmap (buttonExecuteHeatmap), DrawScatter
successStoreScatterplot = 'Scatterplot was successfully saved.' # in function: StoreGraphs 
errorStorePath = 'Please check if the path to store the graph has been given.'  # in function: StoreGraphs
errorScatterplot = 'Please select features and execute the Scatterplot.'    # in function: StoreGraphs
successStoreLineplot = 'Lineplot was successfully saved.' # in function: StoreGraphs
errorLineplot = 'Please select features and execute the Lineplot.' # in function: StoreGraphs
successStoreHeatmap = 'Heatmap was successfully saved.' # in function: StoreGraphs
errorHeatmap = 'Please select features and execute the Heatmap' # in function: StoreGraphs
successStore3dGraph = '3D Graph was successfully saved.' # in function: StoreGraphs
error3dGraph = 'Please select features and execute the 3D Graph.'   # in function: StoreGraphs
errorScatterFeature = 'Please only select up to five features'  # in function: DrawScatter
errorLineplotFeature = 'Please, only select one feature for the Line plot'  # in function: DrawLineplot

################### Data Storage ###################################
successStoreDataset = 'Dataset was successfully stored.'    # in function: SaveDataset 
errorFileFormat = 'Please check whether the file format has been selected.' # in function: SaveDataset
errorFilepath = 'Please check whether the file path has been entered.'  # in functions: SaveDataset, CreateDocumentSummary
errorFilename = 'Please check whether the file name has been entered.' # in functions: SaveDataset, CreateDocumentSummary
error = 'An error has occurred! Please restart the app'     # in function: SaveDataset
successStoreReport = 'Summary Report was successfully stored.' # in function: CreateDocumentSummary

savedContact = 'Contact information has been saved.'
problemContact = 'There has been a problem with saving the contact details. Please check if you filled out the contact information input fields.'

confirm = 'Do you really want to save your contact information?'
missingContactType = 'Please select a contact type in the dropdown.'