from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
import openpyxl
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains


# 函数装饰器，统一处理错误信息
def try_to_run(fun):
    def decorate(*args, **kwargs):
        force_quit_flag = 1
        while True:
            try:
                print(fun.__name__)
                return fun(*args, **kwargs)
            except Exception as e:
                force_quit_flag += 1
                if force_quit_flag > 10:
                    raise Exception("函数{0}运行时失败次数过多,终止尝试".format(fun.__name__))
                print('执行{0}失败，将重试！'.format(fun.__name__))
                time.sleep(1)
                continue

    return decorate


# 获取Chrome的webdriver
def get_chrome_web_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    # 不自动关闭窗口
    options.add_experimental_option('detach', True)
    # 窗口最大化
    options.add_argument('--start-maximized')
    chrome_web_driver_path = '/chromedriver'
    chrome_service = Service(chrome_web_driver_path)
    chrome_driver = webdriver.Chrome(service=chrome_service, options=options)
    chrome_driver.set_window_size(360, 1200)
    return chrome_driver


# 首次打开，同意协议并移除广告
@try_to_run
def agree_protocol_and_remove_ads(web_driver) -> None:
    web_driver.find_element(By.XPATH,
                            "//div[@class='jt-card cookie-policy']/div[@class='jt-card__footer']/button").click()
    time.sleep(1)
    ActionChains(web_driver).move_by_offset(180, 300).click().perform()
    time.sleep(2)
    web_driver.back()


# 打开出发城市
@try_to_run
def open_choose_start_city_page(web_driver) -> None:
    web_driver.find_element(By.XPATH, "//div[@class='airport-picker__airport']").click()


# 打开目的地城市
@try_to_run
def open_choose_dst_city_page(web_driver) -> None:
    web_driver.find_element(By.XPATH, "//div[@class='airport-picker__airport airport-picker__airport--dst']").click()


# 选择目标城市
@try_to_run
def choose_target_city(web_driver, city) -> bool:
    input_elem = web_driver.find_element(By.XPATH, "//input[@class='jt-cityHead-input']")
    input_elem.clear()
    input_elem.send_keys(city)
    time.sleep(1)
    drop_list = web_driver.find_elements(By.XPATH, "//div[@class='jetair-widget-citys-searchlist']/div/ul/li")
    if len(drop_list) == 0:
        return False
    drop_list[0].click()
    return True


# 点击搜索
@try_to_run
def click_into_search_content(web_driver) -> None:
    web_driver.find_element(By.CLASS_NAME, "search-btn").click()


@try_to_run
def open_date_picker_page(web_driver) -> None:
    web_driver.find_element(By.CLASS_NAME, "flightOrgDatewrap").click()


@try_to_run
def choose_date(web_driver, target_date) -> None:
    date_arr = target_date.split('-')
    month_target = '{0}年{1}月'.format(date_arr[0], date_arr[1])
    month_elems = web_driver.find_elements(By.CLASS_NAME, 'monthItemwrap')
    for month_elem in month_elems:
        if month_elem.find_element(By.CLASS_NAME, 'monthItemHeadContent').text != month_target:
            continue
        day_elems = month_elem.find_elements(By.XPATH, "div[@class='monthTable']/ul/li")
        for day_elem in day_elems:
            if day_elem.get_attribute("data-datestr") == target_date:
                day_elem.click()


if __name__ == '__main__':
    date_arr = ['2023-03-04']
    from_arr = ['杭州','兰州','天津','北京','青岛','西安','南昌','广州','南京','上海','福州','厦门','长春','沈阳','石家庄','郑州','太原']
    # 创建存储xlsx
    excel = openpyxl.Workbook()
    driver = get_chrome_web_driver()
    target_link = 'https://m.flycua.com/h5/#/'
    first = True
    cur_sheet = excel.active
    sheet_count = 1
    for date in date_arr:
        if sheet_count > 1:
            cur_sheet = excel.create_sheet(date)
        cur_sheet.title = date
        cur_sheet.append(["出发地", "出发时间", "到达地", "到达时间", "价格", "原价", "备注"])
        for from_item in from_arr:
            driver.get(target_link)
            if first:
                agree_protocol_and_remove_ads(driver)
                # 此处断点，可手动登录
                first = False
            open_choose_start_city_page(driver)
            if not choose_target_city(driver, from_item):
                continue
            open_choose_dst_city_page(driver)
            choose_target_city(driver, "成都")
            open_date_picker_page(driver)
            choose_date(driver, date)
            click_into_search_content(driver)
            # 解析页面数据
            try_count = 1
            while True:
                tickets = driver.find_elements(By.CLASS_NAME, 'flight-info')
                if len(tickets) == 0:
                    try_count += 1
                    if try_count <= 5:
                        time.sleep(1)
                        continue
                break
            page_content = driver.execute_script("return document.body.innerHTML")
            soup = BeautifulSoup(page_content, 'html.parser')
            flight_info = soup.find_all('div', class_='flight-info')
            for info in flight_info:
                try:
                    from_time = info.select(".flight-info-wrap .flight-info-wrap-dep .flight-info-wrap-time")[0].text
                    from_city_info = info.select(".flight-info-wrap .flight-info-wrap-dep .flight-info-wrap-airport")[
                        0].text.replace('\\x3C!---->', '')
                    dst_city_info = info.select(".flight-info-wrap .flight-info-wrap-arr .flight-info-wrap-airport")[
                        0].text.replace('\\x3C!---->', '')
                    dst_time = info.select(".flight-info-wrap .flight-info-wrap-arr .flight-info-wrap-time")[0].text
                    try:
                        price = info.select(".flight-info-wrap > span > i")[0].text[1:]
                    except Exception as ee:
                        price = '未知'
                    try:
                        airplane_info = info.select(".flight-info-text .flight-info-text-air")[0].text.replace(
                            '\\x3C!---->', '+')
                    except:
                        airplane_info = "未知"
                    try:
                        origin_price = info.select(".flight-info-text .flight-info-text-civil")[0].text.replace(
                            '\\x3C!---->', '+')
                    except:
                        origin_price = '未查询到原价'
                    print([from_time, from_city_info, dst_city_info, dst_time, price, airplane_info, origin_price])
                    cur_sheet.append(
                        [from_city_info, from_time, dst_city_info, dst_time, price, origin_price, airplane_info])
                except Exception as e:
                    continue
            time.sleep(5)
        sheet_count += 1
    excel.save("联合航空各地飞往成都票价.xlsx")
