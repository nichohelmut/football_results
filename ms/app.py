import aa
import xgb_preprocess
import xgb_analysis


class App:
    def __init__(self):
        pass

    def run_bookie(self):
        aa.AA()
        xgb_preprocess.PreProcess()
        xgb_analysis.XGBAnalysis()


bot = App()
bot.run_bookie()
