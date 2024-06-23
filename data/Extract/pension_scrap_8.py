from selenium_sets import selenium_sets

from selenium.webdriver.common.by import By

import time
import pandas as pd

pension = pd.DataFrame(columns=['date', 'name', 'star', 'img', 'lowest_price', 'link'])

driver = selenium_sets()
driver.set_window_size(1920, 1080)

dates = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30','31']#, '06', '07', '08', '09', '10']
'''
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',\
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30','31']'''

for i in range(len(dates)-1):# [1일=> 1~5 페이지=>20개의 호텔 => 140개 정보] * 30일 => 4200개
    # 입실가능날짜 
    date = f"23-08-{dates[i]}"
    BASEURL = f'https://hotels.naver.com/list?placeFileName=place%3ABusan_Province&adultCnt=2&checkIn=2023-08-{dates[i]}&checkOut=2023-08-{dates[i+1]}&includeTax=true&sortField=popularityKR&sortDirection=descending&propertyTypes=34' 
    driver.get(BASEURL)
    time.sleep(15)
    try:
        pages = driver.find_elements(By.CLASS_NAME, 'Pagination_page__bCW45')
    except:
        pass
    else:
        for page in pages:
            page.click()
            time.sleep(10)
            ul = driver.find_element(By.CLASS_NAME, 'SearchList_SearchList__CtPf8')
            li_list = ul.find_elements(By.CLASS_NAME, 'SearchList_HotelItem__aj2GM')
                # [입실 가능날짜, 펜션이름, 별점, 펜션이미지, 최저가, 링크] 
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
                pension.loc[len(pension)] = [date, name, star, img, lowest_price, link] # 제일 뒤에 행 추가
    finally:
        ul = driver.find_element(By.CLASS_NAME, 'SearchList_SearchList__CtPf8')
        li_list = ul.find_elements(By.CLASS_NAME, 'SearchList_HotelItem__aj2GM')
            # [입실 가능날짜, 펜션이름, 별점, 펜션이미지, 최저가, 링크] 
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
            pension.loc[len(pension)] = [date, name, star, img, lowest_price, link] # 제일 뒤에 행 추가
        
# 브라우저 종료
driver.quit()

pension.to_csv('pension_naver_08_30.csv', index=False) # csv파일로 저장, 인덱스 설정안함
