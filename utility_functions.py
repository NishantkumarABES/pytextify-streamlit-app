from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
def initialize_driver(CHROMEDRIVER_PATH, headless = True):
    chrome_options = Options()
    if headless: chrome_options.add_argument('--headless')  
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_transcriptions(driver, video_url,  button1_xpath, button2_xpath, title_xpath):
    driver.get(video_url)
    time.sleep(5)
    video_title = driver.find_element(By.XPATH, title_xpath).text
    time.sleep(2)
    driver.find_element(By.XPATH, button1_xpath).click()
    time.sleep(2)
    driver.find_element(By.XPATH, button2_xpath).click()
    time.sleep(2)
    transcript, index = '', 1
    while True:
        transcript_xpath = f'//*[@id="segments-container"]/ytd-transcript-segment-renderer[{index}]/div/yt-formatted-string'
        try: sentence = driver.find_element(By.XPATH, transcript_xpath).text
        except: break
        transcript = transcript + sentence + '\n'
        index = index + 1
    driver.quit()
    return transcript, video_title  


title_xpath = '//*[@id="title"]/h1/yt-formatted-string'
more_xpath = '//*[@id="expand"]'
show_transcript_xpath = '//*[@id="primary-button"]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]'
CHROMEDRIVER_PATH = r'selenium\chromedriver.exe'
driver = initialize_driver(CHROMEDRIVER_PATH, headless=True)

video_url = "https://www.youtube.com/watch?v=x6TsR3y5Qfg"
transcription, video_title = get_transcriptions(driver, video_url, more_xpath, show_transcript_xpath, title_xpath)

with open(f"transcription.txt", "w") as file:
    file.write(f"Video Title: {video_title}\n\n")
    file.write(f"Transcription:\n")
    file.write(transcription)


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


