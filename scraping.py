import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import confing


def set_driver():
    options = webdriver.ChromeOptions()
    # set hide mode
    options.add_argument("headless")

    return webdriver.Chrome(confing.path_to_driver,
                            chrome_options=options)


def get_soup(driver, url=confing.url):
    driver.get(url)
    content = driver.page_source

    return BeautifulSoup(content, 'html.parser')


def get_data(soup):
    game_stat = []
    # get game id
    item_game_result = soup.find('a',
                                 href=True,
                                 attrs={"class": "graph-label"})
    game_id = item_game_result['href'][7:]
    game_stat.append(game_id)

    # get game result
    game_result = float(item_game_result.find('span').get_text()[:-1])
    game_stat.append(game_result)

    # get game stat
    items_game_stat = soup.find_all(class_='round-stats__list')
    stat_value_list = items_game_stat[0].find_all('b')
    stat_value_list = [str(stat_value)[3:-4] for stat_value in stat_value_list]
    # players
    game_stat.append(int(stat_value_list[0]))
    # items value
    game_stat.append(float(stat_value_list[1]))
    # items
    game_stat.append(int(stat_value_list[2]))

    return game_stat


def get_game_status(soup):
    # get graph status
    graph_element = soup.find('div',
                              attrs={"class": "home-left"})
    return graph_element.find('div')['class'][1]


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


driver = set_driver()
driver.get(confing.url)

timer_get_data = get_sec('00:05:00')
start_time = time.time()
data_list = []

while True:
    current_time = time.time()
    if current_time >= start_time + timer_get_data:
        break

    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='graph-wrapper finish']")))

        soup = get_soup(driver)
        data_list.append(get_data(soup))
        time.sleep(5)
    except:
        time.sleep(5)

driver.close()
driver.quit()
