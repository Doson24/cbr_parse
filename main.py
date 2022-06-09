import datetime

from init_driver_selenium import init_webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from matplotlib import pyplot as plt


def parse_cb(url):
    driver = init_webdriver()
    driver.get(url)
    # driver.set_window_size(1920, 1080)
    # driver.save_screenshot('screen.png')
    tr = driver.find_element(By.CLASS_NAME, 'data').find_elements(By.TAG_NAME, 'tr')
    dates = []
    values = []
    for i in tr[1:]:
        el = i.find_elements(By.TAG_NAME, 'td')
        date = el[0].text
        dates.append(date)
        values.append(el[1].text)
    driver.close()
    print('-'*20, 'Загрузка завершена', '-'*20)
    return dates, values


def transform(arg):
    dates = [pd.to_datetime(el, format='%d.%m.%Y') for el in arg[0]]
    values = [float(el.replace(' ', '').replace(',', '.')) for el in arg[1]]
    data = pd.Series(data=values, index=dates)
    return data


if __name__ == '__main__':
    start_date = '10.10.2007'
    end_date = datetime.date.today().strftime('%d.%m.%Y')
    url = f'https://cbr.ru/hd_base/dv/?UniDbQuery.Posted=True&UniDbQuery.From={start_date}' \
          f'&UniDbQuery.To={end_date}&UniDbQuery.P1=4'
    df = transform(parse_cb(url))

    df.to_csv(f'{start_date} {end_date}.csv')

    df.plot()
    plt.tight_layout()
    plt.show()
