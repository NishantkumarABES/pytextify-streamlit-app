import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def is_valid_email(email):
    if '@' not in email or email.startswith('@') or email.endswith('@'):
        return False
    local_part, domain_part = email.split('@')
    if not local_part or not domain_part:
        return False
    if '.' not in domain_part or domain_part.startswith('.') or domain_part.endswith('.'):
        return False
    if len(local_part) > 64 or len(domain_part) > 255:
        return False
    return True

CHROMEDRIVER_PATH = 'assets/selenium/chromedriver.exe'


def initialize_driver(headless = True):
    chrome_options = Options()
    if headless: chrome_options.add_argument('--headless')  
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_transcript(video_url):
    title_xpath = '//*[@id="title"]/h1/yt-formatted-string'
    more_xpath = '//*[@id="expand"]'
    show_transcript_xpath = '//*[@id="primary-button"]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]'
    driver = initialize_driver() 
    driver.get(video_url)
    time.sleep(5)
    video_title = driver.find_element(By.XPATH, title_xpath).text
    time.sleep(2)
    driver.find_element(By.XPATH, more_xpath).click()
    time.sleep(2)
    driver.find_element(By.XPATH, show_transcript_xpath).click()
    time.sleep(2)
    transcript, index = '', 1
    while True:
        transcript_xpath = f'//*[@id="segments-container"]/ytd-transcript-segment-renderer[{index}]/div/yt-formatted-string'
        try:
            sentence = driver.find_element(By.XPATH, transcript_xpath).text
        except:
            break
        transcript += sentence + '\n'
        index += 1
    
    return {'video_title': video_title,'transcription': transcript}

def log_errors(inner):
    def wrapper(*args, **kwargs):
        try:
            return inner(*args, **kwargs)
        except Exception as E:
            ex_type, ex_val, ex_tb = sys.exc_info()
            print(f"An error occurred: {ex_type}, {ex_tb}")
            message = f"{ex_val}, in the function: {inner.__name__}"
            raise Exception(f"ERROR : {message}, {E}")
    return wrapper