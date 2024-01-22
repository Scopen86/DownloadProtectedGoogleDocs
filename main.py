from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

input_string = input("Nhập links google docs (phân cách bằng dấu ', ')")
URLs = []
URLs = input_string.split(", ")

for i in range(len(URLs)):
    #disable javascript
    options = Options()
    options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.javascript": 2,
    })
    driver = webdriver.Chrome(options)

    #modify the URL 
    #URL = URLs[i].replace("/edit?usp=drive_link", "/mobilebasic")
    main_url, junk = URLs[i].split("/edit")
    main_url = main_url + "/mobilebasic"
    driver.minimize_window()
    driver.get(main_url)
    print(main_url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div")))
    time.sleep(3)

    #get page title
    title = driver.title.replace(".doc", "")
    
    #copy the contents of the docs
    actions = ActionChains(driver)

    actions.key_down(Keys.CONTROL)
    actions.send_keys("a")
    actions.key_down(Keys.CONTROL)
    actions.send_keys("c")
    actions.key_up(Keys.CONTROL)
    actions.perform()

    driver.close()

    #Open another instance with javascript enabled
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\Scopen\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument('--profile-directory=Default')
    options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.javascript": 1,
    })

    driver = webdriver.Chrome(options)
    driver.minimize_window()
    driver.get("https://docs.google.com/document/u/0/create?usp=docs_home&ths=true")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="docs-title-widget"]/input')))

    #correct bug: cursor focus on the address bar
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.BACK_SPACE)
    actions.perform()


    #paste the contents of the docs
    canvas = driver.find_element(By.XPATH, '//*[@id="kix-appview"]/div[6]/div/div[1]/div[1]')
    canvas.click()
    time.sleep(1)

    actions.key_down(Keys.CONTROL)
    actions.send_keys("v")
    actions.key_up(Keys.CONTROL)
    actions.perform()
    time.sleep(2)

    #rename
    title_bar = driver.find_element(By.XPATH, '//*[@id="docs-title-widget"]/input')
    title_bar.click()
    title_bar.send_keys(title)
    title_bar.send_keys(Keys.ENTER)


    #check if the doc is properly saved
    WebDriverWait(driver,360).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="docs-save-indicator-badge" and @aria-label = "Trạng thái của tài liệu: Đã lưu vào Drive."]' )))
    saved_status = driver.find_element(By.XPATH, '//*[@id="docs-save-indicator-badge"]').get_attribute("aria-label") 
    print(saved_status)


    #download as .docx
    actions.key_down(Keys.ALT)
    actions.send_keys("f")
    actions.key_up(Keys.ALT)
    actions.perform()
    actions.send_keys("d")
    actions.perform()
    actions.send_keys("x")    
    actions.perform()
    time.sleep(5)

    #open the next link
    driver.get(URLs[i+1])
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="docs-title-widget"]/input')))
    time.sleep(5)

    driver.close()



