import sys
from sqlalchemy import create_engine
import pandas as pd
import os


class MySQLDatabase:
    def __init__(self):
        try:
            self.dbname = os.getenv("RDS_1_DB_NAME")
            self.host = os.getenv("RDS_1_HOST")
            self.port = '3306'
            self.user = os.getenv("RDS_1_USER")
            self.pwd = os.getenv("RDS_1_PASSWORD")

        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    def write(self, df):
        try:
            print("Connecting to Database")
            url = f'mysql+pymysql://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.dbname}'
            engine = create_engine(url)
            for i, row in df.iterrows():
                sql = "SELECT * FROM `bookie` WHERE `id` = '{}'".format(row.id)
                found = pd.read_sql_query(sql, engine)
                if len(found) == 0:
                    df.iloc[i:i + 1].to_sql(name="bookie", if_exists='append', con=engine)
            print("Successfully wrote to Database")
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    def get(self, table):
        """
        Gets a dataframe from source table
        :input: table name
        :return: dataframe
        """
        try:
            print("Connecting to Database and geting results")
            query = f'SELECT * FROM bookie'
            url = f'mysql+pymysql://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.dbname}'
            engine = create_engine(url)
            df = pd.read_sql_query(query, engine)
            return df
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)
