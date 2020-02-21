from selenium import webdriver
from bs4 import BeautifulSoup
import confing

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(confing.path_to_driver,
                          chrome_options=options)
driver.get(confing.url)

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

items_game_result = soup.find_all('a',
                                  href=True,
                                  attrs={"class": "graph-label"})

game_ids = [item['href'][7:] for item in items_game_result]
print(game_ids)

game_results = [float(item.find('span').get_text()[:-1]) for item in items_game_result]
print(game_results)

items_game_statistic = soup.find_all(class_='round-stats__list')

stat_name_list = [str(stat_name)[6:-7] for stat_name in
                  items_game_statistic[0].find_all('span')]
print(stat_name_list)

stat_value_list = [float(str(stat_value)[3:-4]) for stat_value in items_game_statistic[0].find_all('b')]
print(stat_value_list)

driver.quit()
