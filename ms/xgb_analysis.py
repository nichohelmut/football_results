import xgboost as xgb
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
from sklearn.linear_model import LogisticRegression
import clustering as cl
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
import warnings

warnings.filterwarnings('ignore')


class XGBAnalysis:
    def __init__(self):
        self.X_with_columns = pd.read_pickle("pickle_files/X.pkl")
        self.Z_with_columns = pd.read_pickle("pickle_files/Z.pkl")

        columns_to_drop = []

        self.X_with_columns.drop(columns_to_drop, axis=1, inplace=True)
        self.Z_with_columns.drop(columns_to_drop, axis=1, inplace=True)

        self.X = np.array(self.X_with_columns)
        self.Y = np.array(pd.read_pickle("pickle_files/Y.pkl"))
        self.Z = np.array(self.Z_with_columns)
        self.df_next_games = pd.read_pickle("pickle_files/next_games.pkl")

    def upper_limits(self):
        print(' ')
        print('______________________________________________________________')

    def under_limits(self):
        print('______________________________________________________________')
        print(' ')

    def k_fold(self):
        kf = KFold(n_splits=4, random_state=0, shuffle=True)
        kf.get_n_splits(self.X)

        for train_index, test_index in kf.split(self.X):
            print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.Y[train_index], self.Y[test_index]

        return X_train, X_test, y_train, y_test

    def xgb_model(self):
        XGB_model = xgb.XGBClassifier(silent=False,
                                      learning_rate=0.005,
                                      colsample_bytree=0.5,
                                      subsample=0.8,
                                      objective='multi:softprob',
                                      n_estimators=1000,
                                      reg_alpha=0.2,
                                      reg_lambda=.5,
                                      max_depth=5,
                                      gamma=5,
                                      seed=82)

        return XGB_model

    def feature_importance(self, model):
        features_names = list(self.X_with_columns.columns)

        importance = np.round(model.feature_importances_, 4)
        dictionary = dict(zip(features_names, importance))
        sorted_dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
        names = []
        values = []

        self.upper_limits()
        for i in range(0, len(importance)):
            print('Feature Importance: {:35} {}%'.format(
                sorted_dictionary[i][0], np.round(sorted_dictionary[i][1] * 100, 4))
            )
            names.append(sorted_dictionary[i][0])
            values.append(np.round(sorted_dictionary[i][1] * 100, 4))
        self.under_limits()

    def xgb_predict(self, model):
        z_pred = model.predict(self.Z)
        xgb_df_next_games = self.df_next_games.copy()
        xgb_df_next_games['predicted_result'] = z_pred
        xgb_df_next_games['tipico quota'] = 0
        xgb_df_next_games['R'] = False

        self.upper_limits()
        print(xgb_df_next_games)
        self.under_limits()
        return xgb_df_next_games

    def xgb_fit(self):
        X_train, X_test, y_train, y_test = self.k_fold()
        eval_set = [(X_train, y_train), (X_test, y_test)]
        XGB_model = self.xgb_model()

        XGB_model.fit(X_train, y_train, eval_metric=["merror", "mlogloss"], eval_set=eval_set, verbose=True)
        y_pred = XGB_model.predict(X_test)
        y_pred_train = XGB_model.predict(X_train)
        accuracy = accuracy_score(y_test, y_pred)
        accuracy_train = accuracy_score(y_train, y_pred_train)

        self.upper_limits()
        print("XGB train Accuracy: %.2f%%" % (accuracy_train * 100.0))
        print("XGB Accuracy: %.2f%%" % (accuracy * 100.0))
        self.under_limits()

        self.feature_importance(XGB_model)
        self.xgb_predict(XGB_model)


bot = XGBAnalysis()
bot.xgb_fit()
