from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os.path
import pickle
import threading
import pandas as pd
members = []

# SetInterval
def setInterval(func,time,startNow=False,amount=0):
    count = 1
    e = threading.Event()
    if startNow:
        func()
        count += 1
    if amount != 0:
        while not e.wait(time) and count <= amount:
            func()
            count += 1
    else: 
        while not e.wait(time):
            func()
        
# GetNumberMembers
def getNumberMembers():
    browser.get("https://www.facebook.com/groups/mixigaming/members")
    sleep(5)
    numberMembers = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[1]/h2/span/span/span/strong"))).text
    result = ""
    for i in range(0, len(numberMembers)):
        if numberMembers[i].isdigit():
            result += numberMembers[i] 
    print(result)   
    members.append(result) 
    
# ScrollToBottom
def scrollToBottom():
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
# Khai bao bien browser
browser = webdriver.Chrome(executable_path="./chromedriver")

# Mo trang Web
browser.get("https://facebook.com")

if os.path.exists("./my_cookie.pkl"):
    # load cookie
    cookies = pickle.load(open("my_cookie.pkl", "rb"))

    for cookie in cookies:
        browser.add_cookie(cookie)

    # refresh the browser
    browser.get("http://facebook.com")
else:
    # Dang nhap
    txtUserName = browser.find_element(By.ID, "email")
    txtPassword = browser.find_element(By.ID, "pass")

    txtUserName.send_keys("dunggamo2000@gmail.com")
    txtPassword.send_keys("Dung@3112")
    txtPassword.send_keys(Keys.ENTER)
    
    sleep(5)
    
    pickle.dump(browser.get_cookies(), open("my_cookie.pkl", "wb"))

# --- Scroll page ---
browser.get("https://www.facebook.com/groups/mixigaming/")
setInterval(scrollToBottom, 4, False, 0) 

# --- Get member and write to csv ---
# setInterval(getNumberMembers, 5, True, 5)
# print(members)
# df = pd.DataFrame(members, columns=['So thanh vien'])
# df.to_csv("Members.csv", index=True)
# Dong trinh duyet
browser.close()
