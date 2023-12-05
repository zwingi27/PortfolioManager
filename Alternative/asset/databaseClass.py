import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from tqdm import tqdm
from psycopg2 import Error

class PostgressHandler:
    def __init__(self,databaseName: str, user: str, password: str, hostname: str, port:int ) -> None:
        self.database = databaseName
        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.connection = None
        self.engine = None

    def _getItems(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
    
    def _getTables(self):
        sql = f'''SELECT "table_catalog","table_schema","table_name","table_type" FROM information_schema.tables;'''
        return self.executeQuery(sql)
    
    def _getColumnNames(self,table: str):
        sql = f'''SELECT * FROM information_schema.columns WHERE table_name = {table};'''
        return self.executeQuery(sql)
    
    
    def createConnection(self):
        try:
            self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.database}')
            self.connection = self.engine.connect()
            print(f'Database {self.database} connected.')
        except(Exception, Error) as error:
                print('No Database connection possible: ', error)
    
    
    def closeConnection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print(f'Database disconnected.')
        else:
            print('No active connection to close.')


    def executeQuery(self, query: str):
            if query.lower().endswith('.sql'): 
                    with open(query, "r") as file:
                        sql = file.read().replace('\n', ' ')
            elif 'SELECT' in query[:10].upper():
                sql = query
            else:
                print(f"Wrong input inserted (No '.sql' file or sql 'select' string: {query})")
                return None
                            
            try:
                for keyword in ['delete', 'update', 'insert']:
                    if keyword in sql.lower():
                        raise ValueError(f"Error: The keyword '{keyword}' is not allowed in this function. Use the apropriate function instead")

                return pd.read_sql(query, self.connection)
            except(Exception, Error) as error:
                print('SQL Error: ', error)
                return None
    
    
    def uploadData(self, df: pd.DataFrame, table: str, chunksize: int =-1, if_exist: str = 'fail', index: bool = False):
            try:
                if chunksize == -1:
                    chunksize = len(df)

                for i in tqdm(range(0, len(df), chunksize)):
                    chunk = df[i:i + chunksize]
                    chunk.to_sql(table, self.engine, if_exists=if_exist, index=index)

                print(f'Upload to {table} successfully finished.')

            except(Exception, Error) as error:
                print('Upload failed: ', error)