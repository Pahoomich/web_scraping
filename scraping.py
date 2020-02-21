from selenium import webdriver
from bs4 import BeautifulSoup
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
    # print(game_id)
    game_stat.append(game_id)

    # get game result
    game_result = float(item_game_result.find('span').get_text()[:-1])
    # print(game_result)
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
    # print(stat_value_list)

    return game_stat


def get_game_status(soup):
    # get graph status
    graph_element = soup.find('div',
                              attrs={"class": "home-left"})
    return graph_element.find('div')['class'][1]


driver = set_driver()

soup = get_soup(driver)
#
print(get_data(soup))

game_status = get_game_status(soup)

print(game_status)

driver.close()
driver.quit()
