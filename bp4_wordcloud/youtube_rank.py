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
#trs = driver.find_elements_by_css_selector('.aos-init')
#print(len(trs))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
channel_list = soup.select('.aos-init')
print(f'Channel list 갯수: {len(channel_list)}')

# 만과 억을 숫자로 바꿔주는 함수
def convert_unit(s):
    s = s.replace('억', '').replace('개','').replace(',','')
    s = s.replace('만', '0000')
    return f'{int(s):,d}'

channels = []
for channel in channel_list:
    category = channel.select_one('p.category').get_text().strip(' \n[]')
    name = channel.select_one('.subject a').text.strip()
    subscriber = convert_unit(channel.select_one('.subscriber_cnt').text)
    view = convert_unit(channel.select_one('.view_cnt').text)
    video = convert_unit(channel.select_one('.video_cnt').text)
    channels.append([category,name,subscriber,view,video])

df = pd.DataFrame(channels, columns=['카테고리','채널명','구독자수','조회수','비디오수'])
df.to_tsv('youtube rank top 100.tsv', sep='\t', index=False)

driver.close()
