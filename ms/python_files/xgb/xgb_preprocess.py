import pandas as pd
import warnings
import os

warnings.filterwarnings('ignore')

PATH = os.path.dirname(os.path.abspath(__file__))
path_to_a_down = os.path.join(PATH, "../auto_download")
path_to_a_down_files = os.path.join(path_to_a_down, "auto_download_files")
path_to_pickle = os.path.join(PATH, "../../pickle_files")
path_to_g_stats = os.path.join(PATH, "../../germany_stats")
path_to_t_stats = os.path.join(path_to_g_stats, "team_stats")
path_to_m_stats = os.path.join(path_to_g_stats, "match_stats")


class PreProcess:
    def __init__(self):
        # TODO: Automize this index int
        self.int_for_test = 1323
        self.int_for_prediction = self.int_for_test - 9
        self.predictable_columns = [
            'Pre-Match PPG (Home)', 'Pre-Match PPG (Away)', 'attendance', 'home_ppg', 'away_ppg',
            'average_goals_per_match_pre_match', 'btts_percentage_pre_match',
            'over_15_percentage_pre_match', 'over_25_percentage_pre_match',
            'over_35_percentage_pre_match', 'over_45_percentage_pre_match',
            'over_15_HT_FHG_percentage_pre_match',
            'over_05_HT_FHG_percentage_pre_match',
            'average_corners_per_match_pre_match',
            'average_cards_per_match_pre_match', 'odds_ft_home_team_win',
            'odds_ft_draw', 'odds_ft_away_team_win', 'odds_ft_over15',
            'odds_ft_over25', 'odds_ft_over35', 'odds_ft_over45', 'odds_btts_yes',
            'odds_btts_no', 'ht_0', 'ht_1', 'ht_2', 'ht_3', 'ht_4', 'awt_0',
            'awt_1', 'awt_2', 'awt_3', 'awt_4', 'AVGHTGDIFF', 'AVGATGDIFF', 'H_result_1',
            'H_result_2', 'A_result_1', 'A_result_2', 'H_HTGDIFF_1', 'H_HTGDIFF_2',
            'A_ATGDIFF_1', 'A_ATGDIFF_2', 'H_AVGHTGDIFF_1', 'A_AVGATGDIFF_1'
        ]

    def load_clean_data(self):
        df_matches_20_21 = pd.read_csv(
            os.path.join(path_to_a_down_files, "germany-bundesliga-matches-2020-to-2021-stats.csv"))
        df_matches_19_20 = pd.read_csv(
            os.path.join(path_to_m_stats, "germany-bundesliga-matches-2019-to-2020-stats.csv"))
        df_matches_18_19 = pd.read_csv(
            os.path.join(path_to_m_stats, "germany-bundesliga-matches-2018-to-2019-stats.csv"))
        df_matches_17_18 = pd.read_csv(
            os.path.join(path_to_m_stats, "germany-bundesliga-matches-2017-to-2018-stats.csv"))
        df_matches_16_17 = pd.read_csv(
            os.path.join(path_to_m_stats, "germany-bundesliga-matches-2016-to-2017-stats.csv"))

        df_all = pd.concat([df_matches_20_21, df_matches_19_20, df_matches_18_19, df_matches_17_18, df_matches_16_17],
                           sort=False)
        df_all = df_all[df_all['status'] != 'suspended']

        df_all.sort_values('timestamp', inplace=True)
        df_all.reset_index(inplace=True)
        df_all.drop('index', axis=1, inplace=True)

        df_all['attendance'][df_all['attendance'] < 0] = 0

        return df_all

    def append_aa_result(self):
        df_teams_aa = pd.read_pickle(os.path.join(path_to_pickle, "df_teams_only_aa.pkl"))

        columns = pd.Series(df_teams_aa.iloc[:, :-1].columns)
        columns_h = list(columns.apply(lambda x: "ht_" + x))
        columns_a = list(columns.apply(lambda x: "awt_" + x))

        df_empty_columns = pd.DataFrame(columns=(columns_h + columns_a))
        df_matches_with_aa = pd.concat([self.load_clean_data(), df_empty_columns], axis=1)

        df_matches_with_aa_complete = df_matches_with_aa.copy()
        df_matches_with_aa_complete = df_matches_with_aa_complete.iloc[:self.int_for_test, :]

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
        df_all.to_pickle(os.path.join(path_to_pickle, 'df_all.pkl'))

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

        return df_all

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
            # n_games = len(df[df[h_or_a_team] == team])
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

    def add_previous_data(self):
        df_last_home_results = self.previous_data_call(self.results_previous_games(), 'home_team_name', 'result', 'H',
                                                       3)
        df_last_away_results = self.previous_data_call(df_last_home_results, 'away_team_name', 'result', 'A', 3)

        df_last_last_HTGDIFF_results = self.previous_data_call(df_last_away_results, 'home_team_name', 'HTGDIFF', 'H',
                                                               3)
        df_last_last_ATGDIFF_results = self.previous_data_call(df_last_last_HTGDIFF_results, 'away_team_name',
                                                               'ATGDIFF',
                                                               'A', 3)

        df_last_AVGFTHG_results = self.previous_data_call(df_last_last_ATGDIFF_results, 'home_team_name', 'AVGHTGDIFF',
                                                          'H',
                                                          2)
        df_last_AVGFTAG_results = self.previous_data_call(df_last_AVGFTHG_results, 'away_team_name', 'AVGATGDIFF', 'A',
                                                          2)

        df_all = df_last_AVGFTAG_results.copy()
        df_all.to_pickle(os.path.join(path_to_pickle, "df_rnn_base.pkl"))

        df_matches_with_aa_numeric = df_all._get_numeric_data()
        df_matches_with_aa_numeric.drop(
            ['timestamp', 'goal_diff', 'result', 'home_team_goal_count', 'away_team_goal_count'], axis=1, inplace=True)
        df_matches_with_aa_numeric.isnull().sum(axis=0)

        return df_matches_with_aa_numeric

    def normalize(self):
        df_matches_with_aa_numeric = self.add_previous_data()
        df_norm = (df_matches_with_aa_numeric - df_matches_with_aa_numeric.min()) / (
                df_matches_with_aa_numeric.max() - df_matches_with_aa_numeric.min())

        return df_norm

    def data_for_predict(self):

        df_next_games_teams = self.append_aa_result().iloc[self.int_for_prediction:, :][
            ['home_team_name', 'away_team_name']]

        df_X = self.normalize()[self.predictable_columns]
        df_X.fillna(0, inplace=True)
        X = df_X.iloc[:self.int_for_prediction, :]
        Y = self.results_previous_games().iloc[:self.int_for_prediction, :]['result']
        Z = df_X.iloc[self.int_for_prediction:, :]

        X = X.iloc[17:, :]
        Y = Y[17:]
        X.to_pickle(os.path.join(path_to_pickle, "X.pkl"))
        Y.to_pickle(os.path.join(path_to_pickle, "Y.pkl"))
        Z.to_pickle(os.path.join(path_to_pickle, "Z.pkl"))
        df_next_games_teams.to_pickle(os.path.join(path_to_pickle, "next_games.pkl"))

        print(' ')
        print('______________________________________________________________')
        print('Transformed, X, Y and Z pickel files in "pickle_files" folder!')
        print('______________________________________________________________')
