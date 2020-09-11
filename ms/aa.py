import pandas as pd
from clustering import clustering as cl
import os
import warnings

warnings.filterwarnings('ignore')

PATH = os.path.dirname(os.path.abspath(__file__))
path_to_a_down = os.path.join(PATH, "auto_download")
path_to_a_down_files = os.path.join(path_to_a_down, "auto_download_files")
path_to_pickle = os.path.join(PATH, "pickle_files")


class AA:
    def __init__(self):
        pass

    def country_df(self, csv):
        df = pd.read_csv(csv)
        df.sort_values('team_name', inplace=True)
        df.reset_index(inplace=True)
        df.drop("index", axis=1, inplace=True)
        return df

    def european_leagues(self):
        df_france = self.country_df(os.path.join(path_to_a_down_files,
                                                 "france-ligue-1-teams-2019-to-2020-stats.csv"))

        df_germany = self.country_df(os.path.join(path_to_a_down_files,
                                                  "germany-bundesliga-teams-2019-to-2020-stats.csv"))

        df_england = self.country_df(os.path.join(path_to_a_down_files,
                                                  "england-premier-league-teams-2019-to-2020-stats.csv"))

        df_italy = self.country_df(os.path.join(path_to_a_down_files,
                                                "italy-serie-a-teams-2019-to-2020-stats.csv"))

        df_spain = self.country_df(os.path.join(path_to_a_down_files,
                                                "spain-la-liga-teams-2019-to-2020-stats.csv"))

        df_all = pd.concat([df_germany, df_england, df_italy, df_spain, df_france], sort=False)
        df_all.reset_index(inplace=True)
        df_all.drop("index", axis=1, inplace=True)
        df_european_leagues = df_all.copy()

        return df_european_leagues

    def climbers(self):
        path_to_g_stats = os.path.join(PATH, "germany_stats")
        path_to_t_stats = os.path.join(path_to_g_stats, "team_stats")

        path_2_bl = os.path.join(path_to_t_stats, "germany-2-bundesliga-teams-2019-to-2020-stats.csv")
        df_teams_last_second = pd.read_csv(path_2_bl)
        df_bielefeld = df_teams_last_second[df_teams_last_second['common_name'] == 'Arminia Bielefeld']

        path_teams_last_first = os.path.join(path_to_t_stats, 'germany-bundesliga-teams-2018-to-2019-stats.csv')
        df_teams_last_first = pd.read_csv(path_teams_last_first)

        df_nueremberg = df_teams_last_first[df_teams_last_first['common_name'] == 'Nürnberg']
        df_hannover = df_teams_last_first[df_teams_last_first['common_name'] == 'Hannover 96']
        df_stuttgart = df_teams_last_first[df_teams_last_first['common_name'] == 'Stuttgart']

        path_teams_last_17_18 = os.path.join(path_to_t_stats, 'germany-bundesliga-teams-2017-to-2018-stats.csv')
        df_teams_last_17_18 = pd.read_csv(path_teams_last_17_18)
        df_hsv = df_teams_last_17_18[df_teams_last_17_18['common_name'] == 'Hamburger SV']

        path_teams_last_16_17 = os.path.join(path_to_t_stats, 'germany-bundesliga-teams-2016-to-2017-stats.csv')
        df_teams_last_16_17 = pd.read_csv(path_teams_last_16_17)
        df_darmstadt = df_teams_last_16_17[df_teams_last_16_17['common_name'] == 'Darmstadt 98']
        df_ingolstadt = df_teams_last_16_17[df_teams_last_16_17['common_name'] == 'Ingolstadt']

        df_league_climbers = pd.concat(
            [df_nueremberg, df_bielefeld, df_hannover, df_stuttgart, df_hsv, df_darmstadt, df_ingolstadt], sort=False)
        df_league_climbers.reset_index(inplace=True)
        df_league_climbers.drop("index", axis=1, inplace=True)
        df_all_climbers = df_league_climbers.copy()

        return df_all_climbers

    def top_leagues_with_climbers(self):
        df_all = pd.concat([self.european_leagues(), self.climbers()], sort=False)
        df_all.reset_index(inplace=True)
        df_all.drop("index", axis=1, inplace=True)
        df_total = df_all.copy()

        return df_total

    def matrix(self):
        df_all = self.top_leagues_with_climbers()
        df_all.set_index("team_name", inplace=True)
        df_all = df_all.T

        df_teams_numerical = df_all.iloc[8:, :]

        df_norm = (df_teams_numerical - df_teams_numerical.min()) / (
                df_teams_numerical.max() - df_teams_numerical.min())

        X = df_norm.to_numpy()

        return X

    def aa_analysis(self):
        archetypal = cl.ArchetypalAnalysis(n_archetypes=5, iterations=25, tmax=300)
        model = archetypal.fit(self.matrix())

        return model

    def archetypal_transform(self):
        A = self.aa_analysis().transform(self.matrix())

        return A

    def data_labels(self, A):
        teamsList = self.top_leagues_with_climbers()['team_name']
        temasColumnOrdering = {x: y for y, x in enumerate(teamsList)}
        labels = {v: k for k, v in temasColumnOrdering.items()}

        # CHANGE HARD CODED RANGE
        for i in range(0, 104):
            print("{:40}".format(labels[i]), end='')
            for j in A[:, i]:
                print("{:.3f} ".format(j), end='')
            print("")

    def run(self):
        A = self.archetypal_transform()
        df_aa_result = pd.DataFrame(data=A.T)
        df_aa_result.columns = df_aa_result.columns.map(str)

        df_teams_with_aa = pd.concat([self.top_leagues_with_climbers(), df_aa_result], axis=1)
        df_teams_only_aa = df_teams_with_aa.iloc[:, 280:]
        df_teams_only_aa['common_name'] = df_teams_with_aa['common_name']
        self.data_labels(A)
        df_teams_only_aa.to_pickle(os.path.join(path_to_pickle, "df_teams_only_aa.pkl"))
