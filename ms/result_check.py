import pandas as pd
from database import MySQLDatabase
from auto_download.footy_download import FootyStats
import os
from datetime import date

PATH = os.path.dirname(os.path.abspath(__file__))
path_to_pickle = os.path.join(PATH, "germany_stats/match_stats")
path_to_actual = os.path.join(path_to_pickle, "match_stats_20_21")


# if date.today().weekday() == 0:
#    # change to os
#     footy = FootyStats(
#         path='/Users/nicholas/Documents/private code/DS/bookie/udacity_bookie/udacity_ML/ms/germany_stats/match_stats/match_stats_20_21//')
#     footy.login()
#     footy.clean_dir()
#     footy.csv_match_actual()


class ResultCheck:
    def __init__(self):
        self.results = pd.read_csv(os.path.join(path_to_actual, "germany-bundesliga-matches-2020-to-2021-stats.csv"))

    def read_from_db(self):
        global db
        db = MySQLDatabase()
        df = db.get('bookie')

        return df

    def actual_results(self):
        df = self.results
        print('pimmel9')
        print(df)
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
        df = self.read_from_db()
        print('pimmel8')
        print(df)
        df_actual_rows = self.actual_results().loc[list(df['index'])]
        l_result_last_game = list(df_actual_rows['result'])
        df['real_result'] = l_result_last_game
        # df.drop('level_0', axis=1, inplace=True)
        df = df.drop_duplicates(subset=['index'], keep='last')
        print('pimmel5')
        print(df)
        db.write(df)

# bot = ResultCheck()
# bot.update_mysql()
