import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from utils.chrome_driver import ChromeBrowserDriverHelper

options = ChromeBrowserDriverHelper.get_options()
options.add_argument('--window-size={},{}'.format(390, 844))
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
driver = ChromeBrowserDriverHelper.get_with_options('../chromedriver', options)
base_url = 'https://m.bilibili.com/video/BV1XQ4y1d7BB/?spm_id_from=333.337.search-card.all.click&vd_source=daa8c9c63a701936aff9e99505684e67'
driver.get(base_url)
# 此处停顿10秒，等待弹框自动关闭
time.sleep(5)
driver.find_element(By.CLASS_NAME, 'light').click()
time.sleep(2)
driver.find_element(By.CLASS_NAME, 'to-see').click()
time.sleep(2)
page_content = driver.execute_script("return document.body.innerHTML")
soup = BeautifulSoup(page_content, 'html.parser')
print(soup.select(".mplayer-video-wrap > video")[0].get('src'))
