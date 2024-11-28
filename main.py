# Instagram Block Automation
# Version 1.8

'''
For #Blockout2024
A Script crafted to automate blocking users on instagram
This script uses brave browser with chromium version 126
If you are a Palestine supporter and a developer, feel free to fork the code and make it better
This script is still experimental and can cause errors while running,
If the script throws errors, look at the error in the log-file in log directory.
'''

'''
Instructions
1. Either make changes according to your browser or install brave browser for easier use
2. Install the required modules using pip in command prompt
3. Run the code
'''


# Modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from random import choice, randint

from os import listdir

from stdiomask import getpass

from datetime import datetime

from json import loads

# Vars
with open('res/config.json', 'r') as File_Obj:
    Config_Json = File_Obj.read()

Config = loads(Config_Json)

Buffer = Config['Buffer']
Standard_Wait = Config['Standard_Wait']
Increased_Wait = Config['Increased_Wait']
Buffer_Wait_Lower = Config["Buffer_Wait_Lower"]
Buffer_Wait_Upper = Config["Buffer_Wait_Upper"]

DRIVER = "./Driver/chromedriver.exe"
BRAVE = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
LINK = "http://www.instagram.com"
PROFILE = "https://www.instagram.com/{0}"

USERNAME = str(input("USERNAME: "))
PASSWORD = getpass("PASSWORD: ", '*')

Random_Wait_Times = [x/1000 for x in range(2000, 6001)]

Blocked_List_Exists = False
Blocked = []

if f'{USERNAME}.txt' in listdir('log'):
    Blocked_List_Exists = True

with open('res/Accounts_To_Block.txt', 'r') as File_Obj:
    To_Block = [user.strip('\n') for user in File_Obj.readlines()]

Counter = 0
WaitTime = randint(Buffer_Wait_Lower, Buffer_Wait_Upper)

# XPATH Vars
with open('res\\xpath.json', 'r') as File_Obj:
    XPATHS_Json = File_Obj.read()

XPATHS = loads(XPATHS_Json)

Search_Button_XPATH = XPATHS["Search_Button_XPATH"]
Three_Dots_XPATH = XPATHS["Three_Dots_XPATH"]
Block_Button_XPATH = XPATHS["Block_Button_XPATH"]
Follow_Button_XPATH = XPATHS["Follow_Button_XPATH"]
Block_Confirm_XPATH = XPATHS["Block_Confirm_XPATH"]

# Chrome Options
Chrome_Options = webdriver.ChromeOptions()
Chrome_Options.add_argument("--incognito")
Chrome_Options.add_argument("--enable-chrome-browser-cloud-management")
Chrome_Options.binary_location = BRAVE

# Initialisation
service = Service(executable_path=DRIVER)
Browser = webdriver.Chrome(service=service, options=Chrome_Options)

# Functions
def New_Blocked_List(List):
    with open(f'./log/{USERNAME}.txt', 'w') as File_Obj:
        [File_Obj.write(element + '\n') for element in List]

def Retrive_Blocked_List():
    with open(f'./log/{USERNAME}.txt', 'r') as File_Obj:
        Data = [element.strip('\n') for element in File_Obj.readlines()]
    return Data

def log_error(ERROR):
    Mode = 'a' if f'Error_Log_{USERNAME}.txt' in listdir('./log') else 'w'
    with open(f'./log/Error_Log_{USERNAME}.txt', Mode) as File_Obj:
        time = datetime.now()
        record_time = f"[{time.day}/{time.month}/{time.year} | {time.time().hour}:{time.time().minute}:{time.time().second}]"
        File_Obj.write(f"{record_time}\n---[Error Start Block]---\n{ERROR}\n---[Error End Block]---\n")

def New_List():
    New = []
    for element in To_Block:
        if element not in Blocked:
            New.append(element)
    return New

def RandWait():
    Wait_Time = choice(Random_Wait_Times)
    sleep(Wait_Time)

def Block(USER_LINK):
    Browser.get(USER_LINK)
    
    try:
        WebDriverWait(Browser, Increased_Wait).until(EC.presence_of_element_located((By.XPATH, Three_Dots_XPATH)))
        RandWait()
        Follow_Button = Browser.find_element(By.XPATH, Follow_Button_XPATH)
    except Exception as Error:
        return "404"
    
    if str(Follow_Button.text) == "Unblock":
        RandWait()
        return None
    
    RandWait()
    
    Three_Dots = Browser.find_element(By.XPATH, Three_Dots_XPATH)
    Three_Dots.click()
    WebDriverWait(Browser, Standard_Wait).until(EC.presence_of_element_located((By.XPATH, Block_Button_XPATH)))
    RandWait()
    
    Block_Button = Browser.find_element(By.XPATH, Block_Button_XPATH)
    Block_Button.click()
    WebDriverWait(Browser, Standard_Wait).until(EC.presence_of_element_located((By.XPATH, Block_Confirm_XPATH)))
    RandWait()
    
    Block_Confirm = Browser.find_element(By.XPATH, Block_Confirm_XPATH)
    Block_Confirm.click()
    sleep(4)
        
    return True

# Vars
if Blocked_List_Exists:
    Blocked = Retrive_Blocked_List()
    To_Block = New_List()
    
# Automation Process
Browser.get(LINK)

WebDriverWait(Browser, Standard_Wait).until(EC.presence_of_element_located((By.NAME, "password")))
RandWait()

Username_Input_Element = Browser.find_element(By.NAME, "username")
Username_Input_Element.send_keys(USERNAME)

Password_Input_Element = Browser.find_element(By.NAME, "password")
Password_Input_Element.send_keys(PASSWORD)
RandWait()

Password_Input_Element.send_keys(Keys.ENTER)
WebDriverWait(Browser, Standard_Wait).until(EC.presence_of_element_located((By.XPATH, Search_Button_XPATH)))
RandWait()

print("Press 'Ctrl + c' to stop")

for User in To_Block:
    try:
        Val = Block(PROFILE.format(User))
        if Val == None:
            print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {User} Already Blocked")
            Blocked.append(User)
            Counter += 1

        elif Val == True:
            print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {User} blocked")
            Blocked.append(User)
            Counter += 1
            
        elif Val == "404":
            print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {User} | Account not found (unable to locate button elements)")
            Blocked.append(User)
            Counter += 1
        
        if Counter == Buffer:
            Counter = 0
            sleep(WaitTime)
    
    except KeyboardInterrupt:
        print("[Ctrl + c] received.. stopping now!!")
        New_Blocked_List(Blocked)
        Browser.quit()
        quit()
    
    except Exception as Error:
        print(Error)
        log_error(Error)
        try:
            Browser.get(LINK)
            WebDriverWait(Browser, Standard_Wait).until(EC.presence_of_element_located((By.XPATH, Search_Button_XPATH)))
            RandWait()
        except Exception as Error_2:
            print(Error_2)
            log_error(Error_2)
            New_Blocked_List(Blocked)
            quit()

#Quit
sleep(Standard_Wait * 1.5)
Browser.quit()
New_Blocked_List(Blocked)
