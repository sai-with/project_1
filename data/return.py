from selenium_sets import selenium_sets
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = selenium_sets()
driver.set_window_size(1920, 1080)

flights = pd.DataFrame(columns=['date', 'airline', 'deptime', 'arrtime', 'price'])

dates = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
         '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
         '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

for i in range(len(dates)):
    date = f"2023-08-{dates[i]}"
    BASEURL = f'https://flight.naver.com/flights/domestic/PUS-GMP-202308{dates[i]}?adult=1&fareType=YC'
    driver.get(BASEURL)
    time.sleep(10)

    for scroll_count in range(5):
        print(scroll_count)
        # execute_script: window.scrollTo()로 스크롤 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    try:
        flight_elements = driver.find_elements(By.CLASS_NAME, 'domestic_Flight__sK0eA')
        for flight in flight_elements:
            airline = flight.find_element(By.CLASS_NAME, 'name').text
            deptime = flight.find_elements(By.CLASS_NAME, 'route_time__-2Z1T')[0].text
            arrtime = flight.find_elements(By.CLASS_NAME, 'route_time__-2Z1T')[1].text
            price = flight.find_element(By.CLASS_NAME, 'domestic_num__2roTW').text
            flights.loc[len(flights)] = [date, airline, deptime, arrtime, price]

            print(airline)
            print(deptime)
            print(arrtime)
            print(price)

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

    # 날짜별 크롤링 작업 끝난 후 5초 쉬기
    time.sleep(5)

driver.quit()

flights.to_csv('returns.csv', index=False, encoding='utf-8-sig')