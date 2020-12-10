import sys
from sqlalchemy import create_engine
import pandas as pd
import os
from datalab.context import Context
import google.datalab.storage as storage
import google.datalab.bigquery as bq
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nicholasutikal/Downloads/Footy-946fbff39c9c.json"


class MySQLDatabase:
    def __init__(self):
        try:
            #     self.dbname = os.getenv("RDS_1_DB_NAME")
            #     self.host = os.getenv("RDS_1_HOST")
            #     self.port = '3306'
            #     self.user = os.getenv("RDS_1_USER")
            #     self.pwd = os.getenv("RDS_1_PASSWORD")
            #

            self.gcp_table = os.getenv("GCP_TABLE_1")
            self.footy_project_id = os.getenv("FOOTY_PROJECT_ID")
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    def write(self, df):
        try:
        # print("Connecting to Database")
        #     url = f'mysql+pymysql://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.dbname}'
        #     engine = create_engine(url)
        #     for i, row in df.iterrows():
        #         sql = "SELECT * FROM `bookie` WHERE `id` = '{}'".format(row.id)
        #         found = pd.read_sql_query(sql, engine)
        #         if len(found) == 0:
        #             row.to_frame().T.to_sql(name="bookie", if_exists='append', con=engine)
        #     # df['id2'] = df['id']
        #     # df.to_sql(name="bookie", if_exists='replace', con=engine)
        #     print("Successfully wrote to Database")
        #     df.to_gbq(self.gcp_table,
        #               self.footy_project_id,
        #               chunksize=None,
        #               if_exists='append'
        #               )

            client = bigquery.Client()
            table_id = self.footy_project_id
            # Since string columns use the "object" dtype, pass in a (partial) schema
            # to ensure the correct BigQuery data type.
            job_config = bigquery.LoadJobConfig(schema=[
                bigquery.SchemaField("id", "INT"),
            ])

            job = client.load_table_from_dataframe(
                df, table_id, job_config=job_config
            )

            # Wait for the load job to complete.
            job.result()
            print("Successfully wrote to BigQuery")
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

# def get(self, table):
#     pass
# """
# Gets a dataframe from source table
# :input: table name
# :return: dataframe
# """
# try:
#     print("Connecting to Database and geting results")
#     query = f'SELECT * FROM bookie'
#     url = f'mysql+pymysql://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.dbname}'
#     engine = create_engine(url)
#     df = pd.read_sql_query(query, engine)
#     return df
# except Exception as e:
#     print("Error: {}".format(str(e)))
#     sys.exit(1)
