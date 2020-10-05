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
            print('pimmel3')
            print(df)
            # df.reset_index(drop=True, inplace=True)
            df.to_sql('bookie', con=engine, if_exists='replace')
            # engine.execute("SELECT * FROM bookie").fetchall()
            print("Successfully wrote to Database")
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    # def sql_drop_duplicates(self):
    #     pass

    def get(self, table):
        """
        Gets a dataframe from source table
        :input: table name
        :return: dataframe
        """
        try:
            print("Connecting to Database and geting results")
            query = f'SELECT * FROM bookie.{table}'
            url = f'mysql+pymysql://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.dbname}'
            engine = create_engine(url)
            df = pd.read_sql_query(query, engine)
            #
            # if 'level_0' in list(df.columns):
            #     df.drop('level_0', axis=1, inplace=True)
            #
            # print('pimmel4')
            # print(df)
            return df
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)
