from python_files.aa import AA
from xgb_preprocess import PreProcess
from xgb_analysis import XGBAnalysis
from auto_download.footy_download import FootyStats
from database import MySQLDatabase
from result_check import ResultCheck
from datetime import date


# BEFORE NEW PREDICTION UPDATE INT IN xgb_preprocess!!!elf!1!!
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

    r_check = ResultCheck()
    r_check.update_mysql()


# if date.today().weekday() == 3:
run_bookie()
# elif date.today().weekday() == 0:
check_results()
# else:
#     print('DB is updated or no match day due!')
