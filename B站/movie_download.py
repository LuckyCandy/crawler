import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from utils.chrome_driver import ChromeBrowserDriverHelper
from utils.logger import get_logger
from utils.downloader import Downloader
from common import settings

'''
download_url: B站网页地址【视频观看页面,mobile端m.bilibili.com】
chrome_driver_path: chrome浏览器驱动
'''
download_url = 'https://m.bilibili.com/video/BV1XQ4y1d7BB/?spm_id_from=333.337.search-card.all.click&vd_source' \
               '=daa8c9c63a701936aff9e99505684e67 '

# 以下内容可选择性修改
log = get_logger('bilibili')
options = ChromeBrowserDriverHelper.get_options()
options.add_argument('--autoplay-policy=no-user-gesture-required')
options.add_argument('--window-size={},{}'.format(390, 844))
options.add_argument('--headless')
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 ('
                     'KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
options.add_argument("--mute-audio")
driver = ChromeBrowserDriverHelper.get_with_options(settings.CHROME_DRIVER_PATH, options)

driver.get(download_url)
log.info('开始请求.....')
time.sleep(5)
driver.find_element(By.CLASS_NAME, 'light').click()
log.info('等待网页加载.....')
time.sleep(2)
driver.find_element(By.CLASS_NAME, 'to-see').click()
log.info('网页加载完毕.....')
time.sleep(2)
page_content = driver.execute_script("return document.body.innerHTML")
soup = BeautifulSoup(page_content, 'html.parser')
video_url = soup.select(".mplayer-video-wrap > video")[0].get('src')
store_name = soup.select(".title-name > span")[0].text
log.info('解析下载地址成功.....：%s', video_url)

downloader = Downloader(video_url, store_name)
downloader.set_request_headers({
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 ('
                  'KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
})
downloader.start()
