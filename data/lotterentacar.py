from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import csv

# 브라우저 꺼짐 방지
chrome_options= Options()
chrome_options.add_experimental_option('detach', True)

# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# 크롬 드라이버 자동 설치(직접 다운로드 받지 않아도 됨)
# service= Service(executable_path= ChromeDriverManager(url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.98/win32/chromedriver-win32.zip").install())
# driver= webdriver.Chrome(service= service)
service= Service(ChromeDriverManager(version="114.0.5735.90").install()) # 구글 버전 문제 임시 해결 방안(크롬이 급 업데이트를 해서 맞는 드라이버가 없었음)
driver = webdriver.Chrome(service= service, options= chrome_options)

# 8월 한달 24시간 빌렸을때 자동차 이름, 타입, 비용을 가져온다.
for k in range(1, 31):
    # 웹페이지 해당 주소로 이동
    driver.get('https://www.lotterentacar.net/hp/kor/reservation/index.do?areaFlag=1#') # 롯데 렌터카
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#is-login-popup > div > div.section.type1 > a')))
    driver.implicitly_wait(5) # 웹페이지가 로딩될때까지 5초 기다린다.
    driver.maximize_window() # 화면 최대화
    driver.find_element(By.CSS_SELECTOR, '#is-login-popup > div > div.section.type1 > a').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#area-tab-toggle').click() # 지점 목록 버튼
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#region-1 > li:nth-child(2) > button').click() # 공항 버튼
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#region-2 > li:nth-child(3) > button').click() # 김해 선택
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#marker-60401').click() # 지도에서 선택(새로 추가됨230731)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#tab-1 > button').click() # 다음 버튼
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#tab-2 > button').click() # 다음 버튼
    time.sleep(1)

    try:
        driver.find_element(By.XPATH, f'//*[@id="2023080{k}"]').click() # 대여 일자
        time.sleep(1)
    except:
        driver.find_element(By.XPATH, f'//*[@id="202308{k}"]').click() # 대여 일자
        time.sleep(1)

    try:
        driver.find_element(By.XPATH, f'//*[@id="2023080{k+1}"]').click() # 반납 일자
        time.sleep(1)
    except:
        driver.find_element(By.XPATH, f'//*[@id="202308{k+1}"]').click() # 반납 일자
        time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, '#rentHour').click() # 대여시간 버튼 클릭
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#rentHour-10').click() # 대여시간 선택
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#returnHour').click() # 반납시간 버튼 클릭
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#returnHour-10').click() # 반납시간 선택
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#tab-3 > button').click() # 다음 버튼
    time.sleep(10) # 페이지 로딩 시간이 있으므로 기다린다.

    # 파일 생성(파일경로 설정 필요)
    f= open(f'/어떤 경로/{k}.csv', 'w', encoding= 'CP949', newline='') # 날짜별로 저장됨(8월 2일이면 '2'라는 파일에 저장됨)
    csvWriter= csv.writer(f)

    items = driver.find_elements(By.CLASS_NAME, 'vehicle-div')

    for i, item in enumerate(items):
        name = item.find_element(By.XPATH, f'//*[@id="car-list"]/li[{i + 1}]/label/div[1]/div/b').text
        price = item.find_element(By.XPATH, f'//*[@id="car-list"]/li[{i + 1}]/label/div[1]/div/p').text
        print(name, price)
        # 데이터 쓰기
        csvWriter.writerow([name, price])

    # 파일 닫기
    f.close()
