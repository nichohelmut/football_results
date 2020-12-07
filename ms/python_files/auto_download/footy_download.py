# import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import os


class FootyStats:
    def __init__(self,
                 path='/Users/nicholasutikal/Documents/private code/DS/bookie/udacity_bookie/udacity_ML/football_results/ms/python_files/auto_download/auto_download_files//'):
        self.auto_path = path
        options = Options()
        options.add_argument('start-maximized')
        options.add_argument("disable-infobars")
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": r"{}".format(path),
                 # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=options,
                                       executable_path="/usr/local/bin/chromedriver")
        self.username = os.getenv("FOOTY_USERNAME")
        self.password = os.getenv("FOOTY_PASSWORD")

    def login(self):
        self.driver.get('https://footystats.org/')

        sleep(4)

        login_btn = self.driver.find_element_by_xpath('//*[@id="headerMenu"]/li[3]/a')

        login_btn.click()

        email_in = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_in.send_keys(self.username)

        sleep(2)

        pw_in = self.driver.find_element_by_xpath('//*[@id="password"]')
        pw_in.send_keys(self.password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="register_submit"]')
        login_btn.click()

        sleep(3)

        csv_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[1]/div[5]/a[2]')
        csv_btn.click()

    def clean_dir(self):
        mydir = self.auto_path
        filelist = [f for f in os.listdir(mydir) if f.endswith(".csv")]
        for f in filelist:
            os.remove(os.path.join(mydir, f))

    def csv_match_actual(self):
        csv_de_match = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[30]/div/table/tbody/tr[1]/td[3]/a')
        self.driver.execute_script("arguments[0].click();", csv_de_match)

    def csv_downloads(self):
        self.clean_dir()

        sleep(3)
        # de match
        self.csv_match_actual()

        sleep(2)
        # de teams
        csv_de = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[29]/div/table/tbody/tr[1]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_de)

        sleep(2)
        # england teams
        csv_uk = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[24]/div/table/tbody/tr[2]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_uk)

        sleep(2)
        # france teams
        csv_fr = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[28]/div/table/tbody/tr[1]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_fr)

        sleep(2)
        # italy teams
        csv_it = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[42]/div/table/tbody/tr[1]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_it)

        sleep(4)
        # spain teams
        csv_it = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[74]/div/table/tbody/tr[1]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_it)

        sleep(2)

# bot = FootyStats()
# bot.login()
# bot.csv_downloads()
