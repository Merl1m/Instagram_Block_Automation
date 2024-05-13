# Instagram Block Automation
# Version 1.0

'''
For #Blockout2024
A Script crafted to automate blocking users on instagram
This script uses brave browser with chromium version 124
If you are a Palestine supporter and a developer, feel free to fork the code and make it better
'''

'''
Instructions
1. Update the username and password variables with your account credentials
2. Either make changes according to your browser or install brave browser for easier use
3. Update the account usernames in the file 'Accounts_To_Block.txt'
4. Install the required modules using pip in command prompt
5. Run the code
'''
# Modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from random import choice

from pyautogui import typewrite

# Vars
DRIVER = ".\Driver\chromedriver.exe"
BRAVE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
LINK = "http://www.instagram.com"

USERNAME = "" # UPDATE ME
PASSWORD = "" # UPDATE ME

Random_Wait_Times = [x/1000 for x in range(1000, 5001)]

with open('Accounts_To_Block.txt', 'r') as File_Obj:
    To_Block = [user.strip('\n') for user in File_Obj.readlines()]

# XPATH Vars
Search_Button_XPATH = """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]"""
First_Result_XPATH = """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a[1]/div[1]/div/div/div[2]"""
Follow_Button_XPATH = """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[2]/div/div[1]"""
Three_Dots_XPATH = """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[3]/div/div"""
Block_Button_XPATH = """/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/button[1]"""
Block_Confirm_XPATH = """/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/button[1]"""

# Chrome Options
Chrome_Options = webdriver.ChromeOptions()
Chrome_Options.add_argument("--incognito")
Chrome_Options.binary_location = BRAVE

# Initialisation
service = Service(executable_path=DRIVER)
Browser = webdriver.Chrome(service=service, options=Chrome_Options)

# Functions
def RandWait():
    Wait_Time = choice(Random_Wait_Times)
    sleep(Wait_Time)

def Block(USER):
    Search_Button = Browser.find_element(By.XPATH, Search_Button_XPATH)
    Search_Button.click()
    RandWait()

    typewrite(USER)
    sleep(4)

    First_Result = Browser.find_element(By.XPATH, First_Result_XPATH)
    First_Result.click()
    WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Follow_Button_XPATH)))
    RandWait()

    Follow_Button = Browser.find_element(By.XPATH, Follow_Button_XPATH)
    RandWait()
    
    Three_Dots = Browser.find_element(By.XPATH, Three_Dots_XPATH)
    Three_Dots.click()
    RandWait()
    
    Block_Button = Browser.find_element(By.XPATH, Block_Button_XPATH)
    Block_Button.click()
    RandWait()
    
    Block_Confirm = Browser.find_element(By.XPATH, Block_Confirm_XPATH)
    Block_Confirm.click()
    sleep(4)
    
    Browser.get(LINK)
    WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Search_Button_XPATH)))

# Automation Process
Browser.get(LINK)

WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.NAME, "password")))
RandWait()

Username_Input_Element = Browser.find_element(By.NAME, "username")
Username_Input_Element.send_keys(USERNAME)

Password_Input_Element = Browser.find_element(By.NAME, "password")
Password_Input_Element.send_keys(PASSWORD)
RandWait()

Password_Input_Element.send_keys(Keys.ENTER)
WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Search_Button_XPATH)))
RandWait()

Flag = True
for User in To_Block:
    Block(User)
    if Flag:
        Flag = False
        Notification_Not_Now = Browser.find_element(By.CLASS_NAME, "_a9_1")
        Notification_Not_Now.click()
    RandWait()

#Quit
sleep(15)
Browser.quit()