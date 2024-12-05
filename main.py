from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

URL_STEAM = "https://steamdb.info/"

class SteamBot:
    def __init__(self):
        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_experimental_option('detach',True)
        self.driver = webdriver.Chrome(options=self.browser_options)
        self.names = []
        self.developers = []
        self.current_players = []
        self.peak_players = []
        self.all_time_peak = []

    def get_game_data(self,url_path):
        self.driver.get(url_path)
        time.sleep(1.5)

        go_on = self.driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]/div[1]/table/thead/tr/th[2]/a/span')
        go_on.click()

        time.sleep(1)
        for i in range(1,15):
            game_in = self.driver.find_element(By.XPATH, f'//*[@id="table-apps"]/tbody/tr[{i}]/td[3]/a')
            # //*[@id="table-apps"]/tbody/tr[1]/td[3]/a
            game_in.click()
            time.sleep(1.2)

            # Name
            name = self.driver.find_element(By.XPATH,'//*[@id="main"]/div/div[1]/div/div[1]/div[1]/h1')
            self.names.append(name)

            #Developer
            developer = self.driver.find_element(By.XPATH, '//a[@itemprop="author"]')
            self.developers.append(developer.text)

            # Current players
            current_players = self.driver.find_element(By.XPATH,'//*[@id="charts"]/ul[1]/li[2]/strong')
            self.current_players.append(current_players)

            # 24 hours peak
            hours_peak = self.driver.find_element(By.XPATH, '//*[@id="charts"]/ul[1]/li[3]/strong')
            self.peak_players.append(hours_peak)

            # All peak
            all_peak = self.driver.find_element(By.XPATH,'//*[@id="charts"]/ul[1]/li[4]/strong')
            self.all_time_peak.append(all_peak)

            self.driver.back()
            time.sleep(1.2)

def print_csv(names, developers, current_players, peak_players, all_peak):
    fields_name = ['Name', 'Developer', 'Current Players', 'Peak Players', 'All peak']
    file = 'steam_game_info.csv'

    #writing to csv file
    with open(file,'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields_name)

        for i in range(len(names)):
            row = [names[i],developers[i],current_players[i],peak_players[i],all_peak[i]]
            csvwriter.writerow(row)
    csvfile.close()

bot = SteamBot()
bot.get_game_data(URL_STEAM)
print_csv(names=bot.names,developers=bot.developers,current_players=bot.current_players,peak_players=bot.peak_players,all_peak=bot.all_time_peak)
