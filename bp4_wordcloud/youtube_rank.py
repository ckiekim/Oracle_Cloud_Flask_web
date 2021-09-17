from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')   # 화면없이 실행
options.add_argument('--no-sandbox')
options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome('chromedriver', options=options)

url = 'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page=1'
driver.get(url)
time.sleep(2)

trs = driver.find_elements_by_css_selector('.aos-init')
print(len(trs))

driver.close()
