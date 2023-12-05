from components.packages import *
from classes.databaseClass import PostgressHandler

class DataUploader():
    def __init__(self):
        self.df = None
        self.maxid = None

    def readCsvFile(self,content,sep=";"):
        self.df = pd.read_csv(content,sep=sep)
        print("Data read")
        
    def parseData(self,contents, filename):
        _, contentString = contents.split(',')

        decoded = base64.b64decode(contentString)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')), sep=';', header=0)
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
            
            self.df = df
            self.uploadToDatabase("VR-Smart")
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
    
    def uploadToDatabase(self,tableName):
        dbcon = PostgressHandler(databaseName = "Test", user = "postgres", password = "postgres", hostname = "localhost", port = 5432)
        dbcon.createConnection()
        idquery = f'''SELECT MAX("ID") FROM public."{tableName}"'''
        maxid = dbcon.executeQuery(idquery)[max].values[0]+1
        
        self.transformRaibaData(maxid)
        
        #dbcon.uploadData(df = self.df,table = tableName) #,chunksize: int =-1, if_exist: str = 'fail', index: bool = False)
        dbcon.closeConnection()
            
    def transformRaibaData(self,maxid):
        self.df = self.df
        # df = self.df
        # df.columns = [i[:-1] for i in df.columns]
        # df["Analyse-Fixkosten"] = df["Analyse-Fixkosten"].map({'Ja': True, np.nan: False}).astype(bool)
        # df['Betrag'] = df['Betrag'].str.replace('.','').str.replace(',','.').replace('[\€,]', '', regex=True).astype(float)
        # df["Kontostand"] = df['Kontostand'].str.replace('.','').str.replace(',','.').replace('[\€,]', '', regex=True).astype(float)
        # df["Analyse-Betrag"] = df['Analyse-Betrag'].str.replace('.','').str.replace(',','.').replace('[\€,]', '', regex=True).astype(float)
        # df["index"] = range(maxid,maxid+df.shape[0])
        # self.df = df