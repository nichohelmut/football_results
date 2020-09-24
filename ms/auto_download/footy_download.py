# import requests
from selenium import webdriver
from time import sleep
from .secrets import username, password
from selenium.webdriver.chrome.options import Options
import os


class FootyStats:
    def __init__(self):
        path = '/Users/nicholas/Documents/private code/DS/bookie/udacity_bookie/udacity_ML/ms/auto_download/auto_download_files//'
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

    def login(self):
        self.driver.get('https://footystats.org/')

        sleep(4)

        login_btn = self.driver.find_element_by_xpath('//*[@id="headerMenu"]/li[3]/a')

        login_btn.click()

        email_in = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_in.send_keys(username)

        sleep(2)

        pw_in = self.driver.find_element_by_xpath('//*[@id="password"]')
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="register_submit"]')
        login_btn.click()

        sleep(3)

        csv_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[1]/div[5]/a[2]')
        csv_btn.click()

    def csv_downloads(self):
        mydir = '/Users/nicholas/Documents/private code/DS/bookie/udacity_bookie/udacity_ML/ms/auto_download/auto_download_files//'
        filelist = [f for f in os.listdir(mydir) if f.endswith(".csv")]
        for f in filelist:
            os.remove(os.path.join(mydir, f))

        sleep(3)
        # de match
        csv_de_match = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[24]/div/table/tbody/tr[1]/td[3]/a')
        self.driver.execute_script("arguments[0].click();", csv_de_match)

        sleep(2)
        # de teams
        csv_de = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[24]/div/table/tbody/tr[1]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_de)

        sleep(2)
        # england teams
        csv_uk = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[19]/div/table/tbody/tr[2]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_uk)

        sleep(2)
        # france teams
        csv_fr = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[23]/div/table/tbody/tr[1]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_fr)

        sleep(2)
        # italy teams
        csv_it = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[31]/div/table/tbody/tr[1]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_it)

        sleep(4)
        # spain teams
        csv_it = self.driver.find_element_by_xpath(
            '//*[@id="csv_content"]/div[2]/div[2]/div[53]/div/table/tbody/tr[1]/td[4]/a')
        self.driver.execute_script("arguments[0].click();", csv_it)

        sleep(2)


# bot = FootyStats()
# bot.login()
# bot.csv_downloads()
