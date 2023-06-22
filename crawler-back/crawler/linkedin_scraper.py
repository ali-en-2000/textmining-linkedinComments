import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BSoup

def scrape_linkedin_comments(post_url, linkedin_email, linkedin_password, headless=False, show_replies=True):

    with open("crawlerConfig/config.json") as f:
        Config: dict[str, str] = json.load(f)

    options = Options()
    options.headless = headless
    driver = webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )

    driver.get("https://www.linkedin.com")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, Config["username_name"])))

    username = driver.find_element(By.NAME, Config["username_name"])
    username.send_keys(linkedin_email)

    password = driver.find_element(By.NAME, Config["password_name"])
    password.send_keys(linkedin_password)

    sign_in_button = driver.find_element(By.XPATH, Config["sign_in_button_xpath"])
    sign_in_button.click()

    driver.get(post_url)

    load_more("comments", Config["load_comments_class"], driver)
    if show_replies:
        load_more("replies", Config["load_replies_class"], driver)

    bs_obj = BSoup(driver.page_source, "html.parser")

    comments = bs_obj.find_all("span", {"class": Config["comment_class"]})
    comments = [comment.get_text(strip=True) for comment in comments]
    names = bs_obj.find_all("span", {"class": Config["name_class"]})
    names = [name.get_text(strip=True).split("\n")[0] for name in names]
    
    driver.quit()
    return names, comments 


def load_more(target: str, target_class: str, driver: webdriver.Chrome):
    webdriver_wait = WebDriverWait(driver, 10)
    action = ActionChains(driver)

    try:
        load_more_button = webdriver_wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, target_class))
        )
    except:
        print(f"All {target} are displaying already!")
        return


    while True:
        action.move_to_element(load_more_button).click().perform()
        sleep(2)
        try:
            load_more_button = webdriver_wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, target_class))
            )
        except:
            print(f"All {target} have been displayed!")
            break

