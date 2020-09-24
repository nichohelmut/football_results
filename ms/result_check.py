import pandas as pd
from database import MySQLDatabase
import os

PATH = os.path.dirname(os.path.abspath(__file__))
path_to_pickle = os.path.join(PATH, "germany_stats/match_stats")


class ResultCheck:
    def __init__(self):
        self.results = pd.read_csv(os.path.join(path_to_pickle, "germany-bundesliga-matches-2020-to-2021-stats.csv"))

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
        df = self.read_from_db()
        df = df.drop_duplicates(subset=['index'], keep='last')
        df_actual_rows = self.actual_results().loc[list(df['index'])]
        l_result_last_game = list(df_actual_rows['result'])
        df['real_result'] = l_result_last_game
        df.drop('level_0', axis=1, inplace=True)
        db.write(df)

# bot = ResultCheck()
# bot.update_mysql()
