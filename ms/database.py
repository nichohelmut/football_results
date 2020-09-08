import sys
from sqlalchemy import create_engine
import pandas as pd
import config


class MySQLDatabase:
    def __init__(self):
        try:
            self.dbname = config.db_name
            self.host = config.host
            self.port = '3306'
            self.user = config.user
            self.pwd = config.passwd

        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    def write(self, df):
        try:
            print("Connecting to Database")
            engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}"
                                   .format(user=self.user,
                                           pw=self.pwd,
                                           host=self.host,
                                           db=self.dbname
                                           ))
            df.to_sql('bookie', con=engine, if_exists='append')
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
            print("Connecting to Database")
            query = f'SELECT * FROM bookie.{table}'
            url = f'mysql+pymysql://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.dbname}'
            engine = create_engine(url)
            df = pd.read_sql_query(query, engine)
            print(df)
            return df
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)
