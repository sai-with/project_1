from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


"""
해당 함수는 원활한 Selenium 사용을 위해 설정을 진행하는 함수입니다.
첨부된 주석을 통해 해당 코드의 기능을 확인할 수 있습니다.
"""
def selenium_sets():
    # 크롬 꺼짐 방지 및 크롬창 비활성화
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", False) # 자동종료
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    #driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
    # driver_options = Options()
    # # 하기 코드는 False로 설정시 자동으로 웹 브라우저가 종료될 수 있게 설정합니다.
    # driver_options.add_experimental_option("detach", True) 
    # 하기 코드는 불필요한 경고 메시지가 출력되지 않게 설정합니다.
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
    # 하기 코드는 WebDriver를 자동으로 관리하는 모듈을 호출하여 설치합니다.
    auto_driver = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = auto_driver, options = chrome_options)
    return driver

