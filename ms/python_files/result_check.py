import pandas as pd
from database import MySQLDatabase
from auto_download.footy_download import FootyStats
import os
import sys
from sqlalchemy import create_engine
import time
from datetime import date

PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(PATH)

path_to_pickle = os.path.join(BASE_PATH, "pickle_files")
path_to_match = os.path.join(BASE_PATH, "germany_stats/match_stats")
path_to_actual = os.path.join(path_to_match, "match_stats_20_21")


# if date.today().weekday() == 0:
#     # change to os
#     footy = FootyStats(
#         path='/ms/germany_stats/match_stats/match_stats_20_21//')
#     footy.login()
#     footy.clean_dir()
#     footy.csv_match_actual()


class ResultCheck:
    def __init__(self):
        self.results = pd.read_csv(os.path.join(path_to_actual, "germany-bundesliga-matches-2020-to-2021-stats.csv"))
        try:
            self.dbname = os.getenv("RDS_1_DB_NAME")
            self.host = os.getenv("RDS_1_HOST")
            self.port = '3306'
            self.user = os.getenv("RDS_1_USER")
            self.pwd = os.getenv("RDS_1_PASSWORD")

        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    def read_from_db(self):
        global db
        db = MySQLDatabase()
        df = db.get('bookie')

        return df

    def actual_results(self):
        df = self.results
        df.index = df.index + 1224
        df['goal_diff'] = df['home_team_goal_count'] - df['away_team_goal_count']

        for index, row in df[df['status'] == 'complete'].iterrows():
            if df['goal_diff'][index] > 0:
                df.at[index, 'result'] = 3
            elif df['goal_diff'][index] == 0:
                df.at[index, 'result'] = 2
            else:
                df.at[index, 'result'] = 1

        return df

    def update_mysql(self):
        print("Connecting to Database")
        url = f'mysql+pymysql://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.dbname}'
        engine = create_engine(url)

        df = self.read_from_db()
        df = df.tail(9)
        df_actual_rows = self.actual_results().loc[list(df['index'])]
        l_result_last_game = list(df_actual_rows['result'].astype('Int64'))
        df['real_result'] = l_result_last_game

        try:
            df.drop('level_0', axis=1, inplace=True)
        except:
            pass

        os.environ['TZ'] = 'Europe/Amsterdam'
        time.tzset()
        df["date_time"] = time.strftime('%X %x %Z')

        df.to_sql('my_temp', con=engine, if_exists='replace')

        sql = """
            UPDATE bookie 
            INNER JOIN my_temp ON bookie.id = my_temp.id
            set bookie.real_result = my_temp.real_result, bookie.date_time = my_temp.date_time
            WHERE bookie.id = my_temp.id
        """

        with engine.begin() as conn:
            conn.execute(sql)

        print("Successfully updated Bookie table with real results")
