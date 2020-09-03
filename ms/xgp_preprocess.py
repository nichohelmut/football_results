import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import clustering as cl
import warnings

warnings.filterwarnings('ignore')


class PreProcess():
    def __init__(self):
        self.int_for_test = 1233
        self.int_for_prediction = self.int_for_test - 9

    def load_clean_data(self):
        df_matches_20_21 = pd.read_csv(
            "auto_download/auto_download_files/germany-bundesliga-matches-2020-to-2021-stats.csv")
        df_matches_19_20 = pd.read_csv("germany_stats/match_stats/germany-bundesliga-matches-2019-to-2020-stats.csv")
        df_matches_18_19 = pd.read_csv("germany_stats/match_stats/germany-bundesliga-matches-2018-to-2019-stats.csv")
        df_matches_17_18 = pd.read_csv("germany_stats/match_stats/germany-bundesliga-matches-2017-to-2018-stats.csv")
        df_matches_16_17 = pd.read_csv("germany_stats/match_stats/germany-bundesliga-matches-2016-to-2017-stats.csv")

        df_all = pd.concat([df_matches_20_21, df_matches_19_20, df_matches_18_19, df_matches_17_18, df_matches_16_17],
                           sort=False)
        df_all = df_all[df_all['status'] != 'suspended']

        df_all.sort_values('timestamp', inplace=True)
        df_all.reset_index(inplace=True)
        df_all.drop('index', axis=1, inplace=True)

        df_all['attendance'][df_all['attendance'] < 0] = 0

        return df_all

    def append_aa_result(self):
        df_teams_aa = pd.read_pickle("pickle_files/df_teams_only_aa.pkl")

        columns = pd.Series(df_teams_aa.iloc[:, :-1].columns)
        columns_h = list(columns.apply(lambda x: "ht_" + x))
        columns_a = list(columns.apply(lambda x: "awt_" + x))

        df_empty_columns = pd.DataFrame(columns=(columns_h + columns_a))
        df_matches_with_aa = pd.concat([self.load_clean_data(), df_empty_columns], axis=1)

        df_matches_with_aa_complete = df_matches_with_aa.copy()
        df_matches_with_aa_complete = df_matches_with_aa_complete.iloc[:self.int_for_test, :]

        pre_cols = [col for col in df_matches_with_aa_complete.columns if 'pre' in col]
        PRE_cols = [col for col in df_matches_with_aa_complete.columns if 'Pre' in col]
        aa_cols_home = [col for col in df_matches_with_aa_complete.columns if 'ht_' in col]
        aa_cols_away = [col for col in df_matches_with_aa_complete.columns if 'awt_' in col]

        for index, row in df_matches_with_aa_complete.iterrows():
            teams_aa_score_home = list(
                df_teams_aa[df_teams_aa['common_name'] == row['home_team_name']].iloc[:, :-1].iloc[0])
            teams_aa_score_away = list(
                df_teams_aa[df_teams_aa['common_name'] == row['away_team_name']].iloc[:, :-1].iloc[0])

            df_matches_with_aa_complete.at[index, aa_cols_home] = teams_aa_score_home
            df_matches_with_aa_complete.at[index, aa_cols_away] = teams_aa_score_away

        df_matches_with_aa_complete['HTGDIFF'] = df_matches_with_aa_complete['home_team_goal_count'] - \
                                                 df_matches_with_aa_complete['away_team_goal_count']
        df_matches_with_aa_complete['ATGDIFF'] = df_matches_with_aa_complete['away_team_goal_count'] - \
                                                 df_matches_with_aa_complete['home_team_goal_count']

        return df_matches_with_aa_complete

    def avg_goal_diff(self, df, avg_h_a_diff, a_h_team, a_h_goal_letter):
        """
        input:
            df = dataframe with all results
            avg_h_a_diff = name of the new column
            a_h_team = HomeTeam or AwayTeam
            a_h_goal_letter = 'H' for home or 'A' for away
        output:
            avg_per_team = dictionary with with team as key and columns as values with new column H/ATGDIFF
        """
        df[avg_h_a_diff] = 0
        avg_per_team = {}
        all_teams = df[a_h_team].unique()
        for t in all_teams:
            df_team = df[df[a_h_team] == t].fillna(0)
            result = df_team['{}TGDIFF'.format(a_h_goal_letter)].rolling(4).mean()
            df_team[avg_h_a_diff] = result
            avg_per_team[t] = df_team
        return avg_per_team

    def from_dict_value_to_df(self, d):
        """
        input = dictionary
        output = dataframe as part of all the values from the dictionary
        """
        df = pd.DataFrame()
        for v in d.values():
            df = df.append(v)
        return df

    def goal_diff_calculation(self):
        d_AVGFTHG = self.avg_goal_diff(self.append_aa_result(), 'AVGHTGDIFF', 'home_team_name', 'H')
        df_AVGFTHG = self.from_dict_value_to_df(d_AVGFTHG)
        df_AVGFTHG.sort_index(inplace=True)

        d_AVGFTAG = self.avg_goal_diff(df_AVGFTHG, 'AVGATGDIFF', 'away_team_name', 'A')
        df_all = self.from_dict_value_to_df(d_AVGFTAG)
        df_all.sort_index(inplace=True)
        df_all['AVGATGDIFF'].fillna(0, inplace=True)

        return df_all

    def results_previous_games(self):
        df_all = self.goal_diff_calculation()
        df_all['goal_diff'] = df_all['home_team_goal_count'] - df_all['away_team_goal_count']

        for index, row in df_all[df_all['status'] == 'complete'].iterrows():
            if df_all['goal_diff'][index] > 0:
                df_all.at[index, 'result'] = 3
            elif df_all['goal_diff'][index] == 0:
                df_all.at[index, 'result'] = 2
            else:
                df_all.at[index, 'result'] = 1

    def previous_data(self, df, h_or_a_team, column, letter, past_n):
        """
        input:
            df = dataframe with all results
            a_h_team = HomeTeam or AwayTeam
            column = column selected to get previous data from
        output:
            team_with_past_dict = dictionary with team as a key and columns as values with new
                                  columns with past value
        """
        d = dict()
        team_with_past_dict = dict()
        all_teams = df[h_or_a_team].unique()
        for team in all_teams:
            n_games = len(df[df[h_or_a_team] == team])
            team_with_past_dict[team] = df[df[h_or_a_team] == team]
            for i in range(1, past_n):
                d[i] = team_with_past_dict[team].assign(
                    result=team_with_past_dict[team].groupby(h_or_a_team)[column].shift(i)
                ).fillna({'{}_X'.format(column): 0})
                team_with_past_dict[team]['{}_{}_{}'.format(letter, column, i)] = d[i].result

        return team_with_past_dict

    def previous_data_call(self, df, side, column, letter, iterations):
        d = self.previous_data(df, side, column, letter, iterations)
        df_result = self.from_dict_value_to_df(d)
        df_result.sort_index(inplace=True)

        return df_result

# PreProcess().append_aa_result()
