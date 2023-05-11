from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--window-size=15360,8640")
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('chromedriver', options=chrome_options)

    driver.get(url)

    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CLASS_NAME, "match")))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    matches = soup.select('.match.-complete')

    results = []
    for match in matches:
        players = match.select('.match--player')
        if len(players) == 2:
            player1 = players[0].select_one('title').text.strip()
            player2 = players[1].select_one('title').text.strip()
            score1 = players[0].select_one('.match--player-score').text.strip()
            score2 = players[1].select_one('.match--player-score').text.strip()
            results.append([player1, player2, score1 + '-' + score2])

    driver.quit()

    return results

if __name__ == '__main__':
    results = scrape("https://hitboxarena.challonge.com/MoMnewyearsspectacular")
    print(len(results))
