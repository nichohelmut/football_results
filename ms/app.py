from aa import AA
from xgb_preprocess import PreProcess
from xgb_analysis import XGBAnalysis
from auto_download.footy_download import FootyStats
from database import MySQLDatabase
from datetime import date


def run_bookie():
    if date.today().weekday() == 3:
        stats = FootyStats()
        stats.login()
        stats.csv_downloads()

    archetype = AA()
    archetype.run()

    prepro = PreProcess()
    prepro.data_for_predict()

    model = XGBAnalysis()
    model.xgb_fit_and_predict()


def check_results():
    db = MySQLDatabase()
    db.get('bookie')


if date.today().weekday() == 3:
    run_bookie()
else:
    check_results()
