import os.path

import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import openpyxl

from common import settings
from utils.chrome_driver import ChromeBrowserDriverHelper

'''爬取携程票价信息'''

# 创建存储xlsx
excel = openpyxl.Workbook()

# 初始化Driver
options = ChromeBrowserDriverHelper.get_options()
options.add_argument('--start-maximized')
options.add_argument('--headless')
options.add_argument("--disable-popup-blocking")
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 ('
                     'KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
driver = ChromeBrowserDriverHelper.get_with_options(settings.CHROME_DRIVER_PATH, options)

# 出发日期
date_arr = ['2023-03-31']
# 目的地
dst_dict = {
    "TSN": "天津"
}

# 首个sheet无需创建
sheet_count = 1
cur_sheet = excel.active
for date in date_arr:
    if sheet_count > 1:
        cur_sheet = excel.create_sheet(date)
    cur_sheet.title = date
    cur_sheet.append(["航空公司", "出发地", "到达地", "出发时间", "到达时间", "价格", "备注"])

    for dst in dst_dict:
        url = 'https://flights.ctrip.com/online/list/oneway-%s-ctu?depdate=%s&cabin=y_s_c_f&adult=1&child=0&infant=0&containstax=1' % (
        dst.lower(), date)
        print(url)
        driver.get(url)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0)")

        # 循环滚动，否则拿不到完整数据
        while True:
            driver.execute_script("window.scrollBy(0, 350)")
            time.sleep(1)
            # 当达到文档底部时停止
            if driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight"):
                break

        flight_detials = driver.find_elements(By.CLASS_NAME, 'flight-detail')
        flight_prices = driver.find_elements(By.CLASS_NAME, 'flight-operate')
        flight_airlines = driver.find_elements(By.CLASS_NAME, 'flight-airline')

        for i, (flight_detial, flight_price, flight_airline) in enumerate(
                zip(flight_detials, flight_prices, flight_airlines)):
            flight_detial_text = flight_detial.get_attribute('innerText')
            flight_airline = flight_airline.get_attribute('innerText').split('\n')[0]
            try:  # 经停航班会有更多的返回值 不考虑经停航班
                plane_dt, plane_dl, plane_at, plane_al = flight_detial_text.split("\n")
            except:
                continue
            price_arr = flight_price.get_attribute('innerText').split('\n')
            Price = price_arr[0][1:-1]
            Discount = price_arr[1] if len(price_arr) > 1 else '无'
            cur_sheet.append([flight_airline, dst_dict[dst] + plane_dl, plane_al, plane_dt, plane_at, Price, Discount])
            print([flight_airline, dst_dict[dst] + plane_dl, plane_al, plane_dt, plane_at, Price, Discount])
    sheet_count += 1
excel.save(os.path.join(settings.RESOURCE_PATH, "携程各地飞往重庆票价.xlsx"))






