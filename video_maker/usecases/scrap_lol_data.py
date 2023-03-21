import os
from time import sleep
from selenium.webdriver.common.by import By
from entities.data_scrapper import DataScrapper
from entities.match_data import MatchData, Player
from usecases.data import save


class ScrapLolData(DataScrapper):
    def __init__(self) -> None:
        super().__init__()
        # URL
        self.__replay_file_dir = os.path.abspath(r'.\media\replays')
        self.__url = 'https://www.leagueofgraphs.com/replays/with-high-kda/grandmaster/sr-ranked'
        # self.__url = 'https://www.leagueofgraphs.com/ko/replays/all/kr/challenger/sr-ranked'
        # self.__url = 'https://www.leagueofgraphs.com/replays/all/kr/challenger/sr-ranked'
        self.__champions_xpath_selector = '//*[contains(concat( " ", @class, " " ), concat( " ", "relative", " " ))]//img'
        self.__match_table_selector = '//*[contains(concat( " ", @class, " " ), concat( " ", "matchTable", " " ))]'
        self.__region_xpath = '//*[(@id = "mainContent")]//a'
        self.__watch_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "replay_watch_button", " " ))]'
        self.__download_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "replayDownloadButton", " " ))]'
        self.match_data: MatchData = {
            "team1": {
                "players": []
            },
            "team2": {
                "players": []
            }
        }

    def get_match_data_and_download_replay(self) -> None:
        print('staring get data and donwload replay...')
        self.driver.get(self.__url)
        table = self.driver.find_element(
            by=By.XPATH, value=self.__match_table_selector)
        text_list = table.text.split('\n')
        self.match_data['team1']['result'] = text_list[0].split(' ')[0]
        self.match_data['team2']['result'] = text_list[0].split(' ')[-1]
        duration = text_list[0].split(' ')[3][1:-1]
        self.match_data['duration'] = duration
        patch = text_list[-1].split(' ')[1][1:-1]
        self.match_data['patch'] = patch
        elements = self.driver.find_elements(by=By.XPATH, value=self.__champions_xpath_selector)
        elements[0].get_dom_attribute('title')
        champions = self.__get_champions_names(elements=elements)
        # print("this is text_list:\n\n",text_list,"\n\n end")
        self.match_data['team1']['players'] = self.__create_team_one(
            text_list=text_list, champions=champions)
        self.match_data['team2']['players'] = self.__create_team_two(
            text_list=text_list, champions=champions)
        mvp_data = self.__get_mvp_data(self.match_data)
        self.match_data['mvp'] = self.match_data[mvp_data['team']]['players'][mvp_data['player_index']]
        self.match_data['loser'] = self.match_data[mvp_data['loser_team']]['players'][mvp_data['player_index']]['champion']
        self.match_data['player_role'] = mvp_data['player_role']
        self.match_data['player_index'] = str(
            int(mvp_data['player_index']) + 1)
        region_link = self.driver.find_element(
            by=By.XPATH, value=self.__region_xpath)
        link_array = region_link.get_property('href').split('/')
        self.match_data['region'] = link_array[4].upper()
        # Save Data
        save(self.match_data)
        print('saved information')
        print('Starting game download')
        self.__remove_match()
        self.__download_match()
        self.quit()

    def __get_champions_names(self, elements: list) -> list[str]:
        champions = []
        for i in range(0, 38):
            if elements[i].get_dom_attribute('title') is not None:
                champions.append(elements[i].get_dom_attribute('title'))
        return champions

    def __create_player(self, name: str, kda: str, rank: str, champion: str) -> Player:
        print("creating player:",name,kda,rank,champion)
        return {
            "name": name,
            "kda": kda,
            "rank": rank,
            "champion": champion
        }

    def __create_team_one(self, text_list: list, champions: list) -> list[Player]:
        team_one = []
        print("====team x======")
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[2]/td[1]/div/div[2]")
        print(common.text.split())

        name1=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda1=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[2]/td[2]/div[1]").text
        rank1=common.text.split()[-1]
        
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[3]/td[1]/div/div[2]")
        print(common.text.split())
        name2=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda2=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[3]/td[2]/div[1]").text
        rank2=common.text.split()[-1]
        
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[4]/td[1]/div/div[2]")
        print(common.text.split())
        name3=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda3=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[4]/td[2]/div[1]").text
        rank3=common.text.split()[-1]
        
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[5]/td[1]/div/div[2]")
        print(common.text.split())
        name4=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda4=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[5]/td[2]/div[1]").text
        rank4=common.text.split()[-1]
        
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[6]/td[1]/div/div[2]")
        print(common.text.split())
        name5=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda5=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[6]/td[2]/div[1]").text
        rank5=common.text.split()[-1]
        
        team_one.append(self.__create_player(name=name1, kda=kda1, rank=rank1,champion=champions[0]))
        team_one.append(self.__create_player(name=name2, kda=kda2, rank=rank2, champion=champions[2]))
        team_one.append(self.__create_player(name=name3, kda=kda3, rank=rank3, champion=champions[4]))
        team_one.append(self.__create_player(name=name4, kda=kda4, rank=rank4, champion=champions[6]))
        team_one.append(self.__create_player(name=name5, kda=kda5, rank=rank5, champion=champions[8]))
        return team_one

    def __create_team_two(self, text_list: list, champions: list) -> list[Player]:
        team_two = []
        print("====team y======")
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[2]/td[6]/div/div[2]")
        print(common.text.split())
        name1=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda1=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[2]/td[5]/div[1]").text
        rank1=common.text.split()[-1]
        
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[3]/td[6]/div/div[2]")
        print(common.text.split())
        name2=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda2=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[3]/td[5]/div[1]").text
        rank2=common.text.split()[-1]
        
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[4]/td[6]/div/div[2]")
        print(common.text.split())
        name3=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda3=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[4]/td[5]/div[1]").text
        rank3=common.text.split()[-1]
        
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[5]/td[6]/div/div[2]")
        print(common.text.split())
        name4=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda4=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[5]/td[5]/div[1]").text
        rank4=common.text.split()[-1]
        
        common=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[6]/td[6]/div/div[2]")
        print(common.text.split())
        name5=common.find_element(by=By.XPATH, value="./*[1]").text.split("\n")[0]
        kda5=self.driver.find_element(by=By.XPATH, value="//*[@id='mainContent']/div[1]/table/tbody/tr[6]/td[5]/div[1]").text
        rank5=common.text.split()[-1]
        
        team_two.append(self.__create_player(name=name1, kda=kda1, rank=rank1,champion=champions[1]))
        team_two.append(self.__create_player(name=name2, kda=kda2, rank=rank2, champion=champions[3]))
        team_two.append(self.__create_player(name=name3, kda=kda3, rank=rank3, champion=champions[5]))
        team_two.append(self.__create_player(name=name4, kda=kda4, rank=rank4, champion=champions[7]))
        team_two.append(self.__create_player(name=name5, kda=kda5, rank=rank5, champion=champions[9]))
        return team_two

    def __get_mvp_data(self, match_data):
        team = ''
        kdas = []
        if match_data['team1']['result'] == 'Victory':
            for player in match_data['team1']['players']:
                team = 'team1'
                loser_team = 'team2'
                print(player['kda'])
                kdas.append(int(player['kda'].split(' ')[0]))
        else:
            for player in match_data['team2']['players']:
                team = 'team2'
                loser_team = 'team1'
                kdas.append(int(player['kda'].split(' ')[0]))
        player_index = kdas.index(max(kdas))
        roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
        return {
            "team": team,
            "player_index": player_index,
            "loser_team": loser_team,
            "player_role": roles[player_index]
        }

    def __download_match(self):
        watch_button = self.driver.find_element(
            by=By.XPATH, value=self.__watch_xpath)
        download_button = self.driver.find_element(
            by=By.XPATH, value=self.__download_xpath)
        self.driver.execute_script("arguments[0].click();", watch_button)
        sleep(1)
        self.driver.execute_script("arguments[0].click();", download_button)
        sleep(20)

    def __remove_match(self):
        file = os.listdir(self.__replay_file_dir)
        if file:
            os.remove(os.path.join(self.__replay_file_dir, file[0]))
