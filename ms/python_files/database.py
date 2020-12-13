import sys
import pandas as pd
import os


class MySQLDatabase:
    def __init__(self):
        try:
            self.gcp_table = os.getenv("GCP_TABLE_1")
            self.footy_project_id = os.getenv("FOOTY_PROJECT_ID")
            # self.footy_db = os.getenv("GCP_DB")
            self.creds = os.getenv("G_CLOUD_CRED_LOC")
            self.full_table_desc = os.getenv("GCP_BOOKIE_TABLE_FULL")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.creds
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    def write(self, df):
        try:
            print("Connecting to Database")
            for i, row in df.iterrows():
                sql = "SELECT * FROM `{}` WHERE `id` = {}".format(self.full_table_desc, row.id)
                found = pd.read_gbq(sql, self.footy_project_id)
                if len(found) == 0:
                    row.to_gbq(self.gcp_table,
                               self.footy_project_id,
                               chunksize=None,
                               if_exists='append'
                               )
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
            print("Connecting to Database and getting results")
            sql = "SELECT * FROM `{}`".format(self.full_table_desc)
            df = pd.read_gbq(sql, self.footy_project_id)
            return df
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)
