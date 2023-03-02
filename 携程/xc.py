import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import openpyxl

'''爬取携程票价信息'''

# 创建存储xlsx
excel = openpyxl.Workbook()

# 初始化Driver
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_argument('--start-maximized')
options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome('/chromedriver', options=options)

# 出发日期
date_arr = ['2023-03-31', '2023-03-15', '2023-03-08', '2023-03-04']
# 目的地
dst_dict = {
    "TSN": "天津", "BJS": "北京", "TAO": "青岛", "SIA": "西安", "LHW": "兰州", "KHN": "南昌", "CAN": "广州",
    "HGH": "杭州",
    "NKG": "南京", "SZV": "苏州", "SHA": "上海", "FOC": "福州", "XMN": "厦门", "CGQ": "长春", "SHE": "沈阳",
    "SJW": "石家庄",
    "CGO": "郑州", "TYN": "太原"
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
excel.save("携程各地飞往重庆票价.xlsx")






