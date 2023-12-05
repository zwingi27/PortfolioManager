"""
========================================================================
Containing general functions in Feature Engineering

"""

from components.packages import *
import webbrowser




def ChangeUnit(dataframe):
    """

    Args:
        dataframe (Dataframe): Dataframe whose unit is to be converted to millimetres.

    Returns:
        data (Dataframe): Dataframe has the unit millimetres.
    """
    
    dfColumns= dataframe.columns
      
    x_help = dataframe[dfColumns[0]].apply(lambda x: float(x.replace("," , "."))*1000)
    y_help =  dataframe[dfColumns[1]].apply(lambda x: float(x.replace("," , "."))*1000)
    z_help = dataframe[dfColumns[2]].apply(lambda x: float(x.replace("," , "."))*1000)               # 3D file
    stress_help = dataframe[dfColumns[3]].apply(lambda x: float(x.replace("," , ".")))
    

    dataframe.insert(0, 'X_Location(mm)', x_help, allow_duplicates=False)
    dataframe.insert(2, 'Y_Location(mm)', y_help, allow_duplicates=False)
    dataframe.insert(4, 'Z_Location(mm)', z_help, allow_duplicates=False) 
    dataframe.insert(6, 'EquivalentStress(Pa)', stress_help, allow_duplicates=False)
   
   
    data= dataframe.drop(dataframe.columns[[1, 3, 5,7]], axis=1)
  
    data = data.round(2)
   
    return data
    


def RenameColumnNames(dataframe):
    """
    Args:
        dataframe (Dataframe): Dataframe whose column names are to be stripped of unnecessary spaces.

    Returns:
        dataframe (Dataframe): Dataframe with column names without unnecassary spaces.
    """
    
    dfColumns= dataframe.columns
    
    lstColumn= []
    for column in dfColumns:                                   # removes unnecessary spaces from column names
        columnNames_help= column.strip(" ")
        lstColumn.append(columnNames_help) 
        
    for i in range(len(dfColumns)):
        dataframe= dataframe.rename(columns= {dfColumns[i]: lstColumn[i]})          # rename the column names
    return dataframe

            
def ChangePath(path):
    """
    Args:
        path (String): Path

    Returns:
        changedPath (String): Path with the correct slashes.
    """
    if "\\" in path:
        changedPath = path.replace('\\', '/')
        return changedPath
    else:
        changedPath = path
        return changedPath
    
    
def StoragenameGraph(graphName, pathImage):
    
    """
    Args:
        graphName (String): Name of the graph.
        pathImage (String): Path where the graph should be saved as an image.
    Returns:
        [type]: [description]
    """
    count_help = 1
    while os.path.isfile(os.path.join(pathImage, 'DAD-GSC_' + graphName + '-' + str(count_help) + '.jpeg')):
        count_help = count_help + 1
    nameImage = 'DAD-GSC_' + graphName + '-' + str(count_help) + '.jpeg'
    return nameImage    
                    
    
# Filter df for specific value in specific feature
def FilterMethod(dataframe, feature, value):
    """
    Args:
        dataframe (Dataframe): Dataframe to perform filter action on.
        feature (String): Name of feature to search for in the dataframe.
        value (String, Integer, Float): Specific value in the column of the feature to filter for.
            
    Returns:
        df (Dataframe)
    """
    
    df = dataframe[dataframe[feature]==value]
    return df


# Pandas Profiling Report
def PandasProfileReport(data, path, reportname):
    """
    Args:
        data (Dataframe): DataFrame containing the data which should be analyzed.        
        path (String): Path where the Profiling Report should be stored.
        reportname (String) Filename of the Profiling Report.

    Returns:
        Pandas Profiling Report HTML and stores it in a local source.
        news (List): Logging statement.  
    """
    
    profile = ProfileReport(data, title=reportname + ' Dataset Profiling Report', explorative=True)
    loc = os.path.join(path,reportname + '_Profiling_Report.html')
    profile.to_file(loc)
    webbrowser.open('file://' + os.path.realpath(os.path.join(path, reportname + '_Profiling_Report.html')))
    news = 'Profile Report finished and stored'
    return news

## SweetViz Report
def SWEETVIZReport(data):
    """
    Args:
        data (Dataframe): DataFrame containing the data which should be analyzed .       
   
    Returns:
        SWEETVIZ Profiling Report HTML and stores it in a local source.
        news (List): Logging Statement.
    """
    
    myReport = sv.analyze(data)  
    myReport.show_html()
    news = 'SWEETVIZ Report finished and stored'
    return news
    
    
# Dataset Storage:
def DataStorage(data, fileFormat, fileName, directory, index = True, sep = ',', orient = None):
    """
    Args:
        data (Dataframe): DataFrame containing the data which should be analyzed.
        fileFormat (String): File format which the data should be saved ('.csv', '.json'')
        fileName (String): Filename of the Dataset.
        directory (String): Directory where the Dataset should be stored.
        index (Boolean, optional): Whether to include the index values in the JSON string. Not including the index (index=False) is only supported when orient is ‘split’ or ‘table’. Default: True.
        sep (String, optional): String of length 1. Field delimiter for the output file..; Default: ','.
        orient (String, optional): Indication of expected JSON string format. Possible Values {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}. Default: None.

    Returns:
        Stores the Dataset with the chosen fileformat in the chosen directory.
        news (List): Logging Statement.
    """
    
    try:
        pathDirectory_help = os.path.join(directory,fileName + fileFormat)
        if fileFormat == '.csv':
            data.to_csv(pathDirectory_help, index = index, sep = sep)
            news = 'Dataset successfully stored as CSV_File in ' + str(pathDirectory_help)
                
        elif fileFormat == '.json':
            if index == False and orient not in ['split', 'table']:
                news = 'Index = "False" is only possible if orient = "split" or "table"'
            else:
                data.to_json(pathDirectory_help, index = index, orient=orient) 
                news = 'Dataset successfully stored as JSON_File in ' + str(pathDirectory_help)
                
        else:
            news = 'Storage format not supported. Choose ".csv" or ".json" instead'
            
    except:
        news = 'Storage failed'
        
    return news
        


## Drop Column
def DropColumn(data, featureList):
    """
    Args:
        data (Dataframe): DataFrame containing the data which should be analyzed.
        featureList (List): List of Features which should be dropped from the data set.

    Returns:
        data (Dataframe): Changed DataFrame.
        news (List): Logging Statement.
    """
    
    news = []
    for feature in featureList:
        try:
            data = data.drop(feature, axis = 1)
            news.append('Feature "' + feature + '" dropped from the dataset')
        except:
            news.append('Feature "' + feature + '" not available in the dataset')
            
    return data, news


## Drop Row
def dropRow(data, rowList, index = 0):
    """
    Args:
        data (Dataframe): DataFrame containing the data which should be analyzed.
        rowList (List): List of row numbers which should be dropped from the dataset.
        index (Integer, optional): Integer that indicates which index (dataframe from file) to use to drop the row.

    Returns:
        data (Dataframe): Changed DataFrame.
        news (List): Logging Statement.
    """
    
    news = []
    for feature in rowList:
        try:
            if index == 0:
                data = data.drop(feature, axis = 0)
                news.append('Row number "' + str(feature) + '" dropped from the dataset')
                
            else:
                row_help = data.loc[(data['Index'] == index) & (data['Counter'] == feature)].index  # get overall row number in df for specific row in specific dataframe
                data = data.drop(row_help, axis = 0)
                news.append('Row number %s dropped from the dataset with the index %s' % (str(feature), str(index)))
                
        except:
            news.append('Row number "' + str(feature) + '" not available in the dataset')
            
    return data, news


## Change Data Types
def TypeChange(data, feature, newtype):
    """
    Args:
        data (Dataframe): Dataframe containing the data which should be analyzed.
        feature (String): Feature whose Type should be changed.
        newtype (String): New feature type. At the moment supported: 'int64', 'float64', 'datetime64[ns, US/Eastern]', 'str'.

    Returns:
        data (Dataframe):  Changed DataFrame.
        news (List): Logging statement.
    """
    
    news = []
    try:
        data[feature] = data[feature].astype(newtype) 
        news.append('Feature "' + feature + '" is now of the type "'+ newtype + '"')
        
    except:
        news.append('Feature "' + feature + '" cannot be transformed to type "'+ newtype + '"')
    return data, news


## Drop Duplicates
def DropDuplicate(data, subsets= None, keeping = 'first',index_ignore=True):
    """
    Args:
        data (Dataframe): Dataframe containing the data which should be analyzed.
        subsets (String, optional): Only consider certain columns for identifying duplicates. Default: Use all columns.
        keeping (String, optional): Determines which duplicates (if any) to keep. Possible values: - first : Drop duplicates except for the first occurrence. 
                                                                                                - last : Drop duplicates except for the last occurrence. 
                                                                                                - False : Drop all duplicates.
        index_ignore (Boolean, optional): If True, the resulting axis will be labeled 0, 1, …, n - 1. Default: True

    Returns:
        data (Dataframe): Changed DataFrame.
        news (List): Logging Statement.
    """
    
    news = []
    try:
        data = data.drop_duplicates(subset =subsets, keep = keeping, ignore_index = index_ignore)
        news.append('All Duplicates got removed')
    except:
        news.append('Duplicates could not be removed')
    return data, news



## Heatmap
def PlotHeatmap(data, method, featureList = None, units=None):
    """
    Args:
        data (Dataframe): DataFrame containing the data which should be analyzed.
        method (String): Name of correlation coefficient to be computed. Available: person, kendall, spearman.
        fetureList (List, optional): Features of Dataframe to be considered for heatmap plot. Default: All features.
        units (Dictionary, Optional): Contains the units of the features. Key=feature, value=unit. Default=None

    Returns:
        figureHeatmap (Figure): Heatmap with the relations between different features in the dataset. 
    """
    if featureList is not None:
        df = pd.DataFrame()              # Dataframe, that only contains the features to be used
        for feature in featureList:
            if feature in data.columns:
                df[feature] = data[feature]
        data = df
    
    if units is not None:
        for column in list(data.columns):
            if column in units.keys():
                data = data.rename(columns={column:column+" [%s]"%(units.get(column))})


    correlationCoefficient_help = data.corr(method=method)
    
    figureHeatmap = go.Figure(data=go.Heatmap(z=correlationCoefficient_help, x=data.columns, y=data.columns, zmin=-1, zmax=1, colorscale='Inferno')) # Heatmap, z: values of correlation matrix, x,y: headings
    for column1 in data.columns:
            for column2 in data.columns:
                
                textcolor_help = '#343a40' # gray-dark
                annotation_help = correlationCoefficient_help.at[column1, column2] # get each value from the correlation matrix
                
                if annotation_help < 0:
                    textcolor_help = '#fff' # white
                    
                if str(annotation_help) != 'nan':
                   annotation_help = round(annotation_help, 3) # round each value to 3 decimal places
                   
                figureHeatmap.add_annotation(x=column1, y=column2, text=str(annotation_help), font={'size': 12, 'color': textcolor_help}, showarrow=False) # add the values as text to the heatmap
    figureHeatmap.update()
    
    return figureHeatmap




## Pairplot    
def PlotScatterPlot(data, featureList=None, units=None):
    """
    Args: 
        data (Dataframe): Dataframe containing the data which should be analyzed.
        fetureList (List, optional): Features of Dataframe to be considered for pair plot. Default: All features.
        units (Dictionary, Optional): Contains the units of the features. Key=feature, value=unit. Default=None
    
    Returns:
        figureScatterPlot (Figure): Pairplots (Scatterplots) of all features versus each other.
    """
    
    if featureList is not None:
        df = pd.DataFrame()              # Dataframe, that only contains the features to be used
        for feature in featureList:
            df[feature] = data[feature]
            df['Index'] = data['Index']
        data = df
        
    if units is not None:
        for feature in list(data.columns):
            if feature in units.keys():
                data = data.rename(columns={feature:feature+" [%s]"%(units.get(feature))})
        
    df_help = data.drop(columns=['Index'])
    plotList = list(combinations(df_help.columns, 2))

    height_help = len(plotList)/2 * 300                   # compute height all plots will need
    if len(plotList) == 1:
        height_help = 300

    countRows_help = int(len(plotList)/2) if len(plotList) %2 == 0 else int(len(plotList)/2)+1 
    figureScatterPlot = subplots.make_subplots(rows = countRows_help, cols = 2, horizontal_spacing = 0.15)
    indexList = list(pd.unique(data['Index']))

    color = {}              # dictionary for color value, so that all data from one file has the same color in all the subplots
    for index in indexList:
        color[index] = 'rgb(%s,%s,%s)' %(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
    
    showlegend = True      
    row_help = 1
    for i in range(len(plotList)):

        if i % 2 == 0:
            column1, column2 = plotList[i]
            for j in indexList: # plot figure for each index
                figureScatterPlot.add_trace(go.Scatter(x=data[data['Index']==j][column1], y=data[data['Index']==j][column2], mode='markers', name='Index'+str(j), legendgroup='index'+str(j), marker=dict(color=color[j]), showlegend=showlegend), row=row_help, col=1)
                figureScatterPlot.update_xaxes(title_text=column1, row=row_help, col=1)
                figureScatterPlot.update_yaxes(title_text=column2, row=row_help, col=1)

        if i == 0:
            showlegend = not showlegend

        if i % 2 != 0:
            column1, column2 = plotList[i]
            for j in indexList: # plot figure for each index
                figureScatterPlot.add_trace(go.Scatter(x=data[data['Index']==j][column1], y=data[data['Index']==j][column2], mode='markers', name='Index'+str(j), legendgroup='index'+str(j),  marker=dict(color=color[j]), showlegend=showlegend), row=row_help, col=2)
                figureScatterPlot.update_xaxes(title_text=column1, row=row_help, col=2)
                figureScatterPlot.update_yaxes(title_text=column2, row=row_help, col=2)

            row_help += 1

    figureScatterPlot.update_layout(height=height_help)         # if height is not specified, subplots will be plotted on top of each other
    
    return figureScatterPlot


# Histogram
def PlotHistogram(data, method, units=None):
    """
    Args:
        data (Dataframe): Dataframe containing the data which should be analyzed.
        method (String): Specifying if histogram or distribution plot is wanted. Available: 'histogram', 'percent', 'probability', 'density', 'probability density'.
        units (Dictionary, Optional): Contains the units of the features. Key=feature, value=unit. Default=None
    
    Returns:
        histogramPlot (Figure): Histogram of all features.  
    """

    if units is not None:
        for column in list(data.columns):
            if column in units.keys():
                data = data.rename(columns={column:column+" [%s]"%(units.get(column))})

    columns_help = data.columns                     # name of columns of dataframe
    histogramPlot = go.Figure()

    if method == 'histogram':
        method = None

    histogramPlot.add_trace(go.Histogram(x=data[columns_help[0]], name=columns_help[0], histnorm=method))                                          # add first Feature to figure (this one is visible in the beginning)
    for col_idx in range(1, len(columns_help)):                                                                                                    # add rest of the features is a loop (they are not visible from the beginning on)
        histogramPlot.add_trace(go.Histogram(x=data[columns_help[col_idx]],  name=columns_help[col_idx], histnorm=method, visible='legendonly'))   # visible='legendonly' hide all traces in Grafik, can only be view when clicked on

    return histogramPlot



## Lineplot
def PlotLinePlot(data, feature, units=None):   
    """
    Args:
        data (Dataframe): DataFrame containing the data which should be analyzed.
        feature (String): Features of Dataframe to be considered for pair plot.
        units (Dictionary, Optional): Contains the units of the features. Key=feature, value=unit. Default=None
        
    Returns:
        figureLinePlot (Figure): Lineplot of all features.  
    """
    if units != None:
        for column in list(data.columns):
            if column in units.keys():
                data = data.rename(columns={column:column+" [%s]"%(units.get(column))})
        if feature in units.keys():
            feature += ' [%s]'%(units.get(feature))
    
    figureLinePlot = px.line(data, x='Counter', y=feature, color='Index')
    figureLinePlot.update_layout(xaxis_title="measuring points")
    
    return figureLinePlot


# Dataset Visualizations
 ## Head
def PreviewData(data,kind = 'head', numberOfLines = 5):
    """
    Args:
        data (Dataframe): DataFrame containing the data which should be analyzed.
        kind (String, optional): Kind of Visualization of the Dataset. Available: - 'head', Default: Returns the first num_lines rows of the dataset
                                                                                - 'tail': Returns the last num_lines rows of the dataset
                                                                                - 'info': Creates a concise summary of a DataFrame. It shoes information about a DataFrame including the index dtype and columns, non-null values and memory usage
                                                                                - 'description': Descriptive statistics include those that summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values
                                                                                - 'dtype': Returns a Series with the data type of each column. The result’s index is the original DataFrame’s columns
        numberOfLines (Integer, optional): Number of rows which should be shown. Default: 5.
    Returns:
        Returns the respective preview of the dataset.    
    """

    if kind == 'head':
        return data.head(numberOfLines)
    elif kind == 'tail':
        return data.tail(numberOfLines)
    elif kind == 'info':
        return data.info()
    elif kind == 'description':
        return data.describe()
    elif kind == 'dtype':
        return data.dtypes
    else:
        print('Error: Wrong kind input. Choose "head" or "tail" instead') 
        


def GetMissingValues(df):
    """
    Args:
        df (Dataframe): Dataframe with missing values.
        
    Returns:
        missingValuesDf (Dataframe): Dataframe of features with missing values.
    """

    missingValue = []
    for col in df.columns:
        if df[col].isna().sum() >0:
            missingValue.append(col)
    return missingValue


def ReduceData(data, percent):
    """
    Args:
        data (Dataframe) : Data frame which should be reduced.
        percent (Integer) : Percentage of data points to reduce (e.g., 50)
        
    Returns:
        df_reduced (Dataframe) : Reduced data frame.
    """
    
    reducedDf = pd.DataFrame()
    for i in pd.unique(data['Index']):
        df_help = data[data['Index']==i]
        sampledDf_help = data[0:1]
        step_help = len(pd.unique(data.Counter))//((len(pd.unique(data.Counter))*percent)//100)
        sampledDf_help = pd.concat((sampledDf_help, df_help[1:-1:step_help]))
        sampledDf_help = pd.concat((sampledDf_help, df_help[-1::]))
        reducedDf = pd.concat((reducedDf, sampledDf_help))
    return reducedDf
        






