from selenium_sets import selenium_sets

from selenium.webdriver.common.by import By

import time
import pandas as pd

hotel = pd.DataFrame(columns=['date', 'name', 'star', 'img', 'lowest_price', 'link'])

driver = selenium_sets()
driver.set_window_size(1920, 1080)

dates = ['26', '27', '28', '29', '30','31']#, '06', '07', '08', '09', '10']
'''
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',\
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30','31']'''
page_idx = [1, 2, 3, 4, 5, 6, 7]
for i in range(len(dates)-1):# [1일=> 1~7 페이지=>20개의 호텔 => 140개 정보] * 30일 => 4200개
    # 입실가능날짜 
    date = f"23-08-{dates[i]}"
    for page in page_idx:
        # 1-2일 2-3일 ~ 30-31일 각각 5페이지씩 스크래핑 (100개씩)(세금포함가격)
        
        BASEURL = f'https://hotels.naver.com/list?placeFileName=place%3ABusan_Province&adultCnt=2&checkIn=2023-08-{dates[i]}&checkOut=2023-08-{dates[i+1]}&includeTax=true&sortField=popularityKR&sortDirection=descending&propertyTypes=0%2C7&pageIndex={page}' 
        driver.get(BASEURL)
        time.sleep(15)
        ul = driver.find_element(By.CLASS_NAME, 'SearchList_SearchList__CtPf8')
        li_list = ul.find_elements(By.CLASS_NAME, 'SearchList_HotelItem__aj2GM')
        # [입실 가능날짜, 호텔이름, 별점, 호텔이미지, 가격, 링크] 
        for li in li_list: # 호텔 하나하나에서
            
            info = li.find_element(By.CLASS_NAME, 'Detail_InfoArea__uZ4qT')
            # 호텔이름
            name = info.find_element(By.TAG_NAME, 'h4').text 
            # 별점
            star = info.find_element(By.CLASS_NAME, 'Detail_score__UxnqZ').text
            
            # 호텔이미지
            img = li.find_element(By.TAG_NAME, 'img').get_attribute('src')
            
            price = li.find_element(By.CLASS_NAME, 'Price_Price__7vul8')
            # 호텔가격
            lowest_price = price.find_element(By.CLASS_NAME, 'Price_show_price__iQpms').text
            # 네이버 예약링크
            link = li.find_element(By.CLASS_NAME, 'SearchList_anchor__rKpmX').get_attribute('href')
            # df에 row 추가
            hotel.loc[len(hotel)] = [date, name, star, img, lowest_price, link]
# 브라우저 종료
driver.quit()

hotel.to_csv('hotel_naver_08_30.csv', index=False)
