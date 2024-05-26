# Instagram Block Automation
# Version 1.6

'''
For #Blockout2024
A Script crafted to automate blocking users on instagram
This script uses brave browser with chromium version 124
If you are a Palestine supporter and a developer, feel free to fork the code and make it better
This script is still experimental and can cause errors while running,
if you are getting xpath error, update the xpath variables below with the new xpath from instagram web.
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

from random import choice, randint

from os import listdir

from stdiomask import getpass

# Vars
DRIVER = ".\Driver\chromedriver.exe"
BRAVE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
LINK = "http://www.instagram.com"
PROFILE = "http://www.instagram.com/{0}"

USERNAME = str(input("USERNAME: "))
PASSWORD = getpass("PASSWORD: ", '*')

Random_Wait_Times = [x/1000 for x in range(2000, 6001)]

Blocked_List_Exists = False
Blocked = []

if f'{USERNAME}.txt' in listdir():
    Blocked_List_Exists = True

with open('Accounts_To_Block.txt', 'r') as File_Obj:
    To_Block = [user.strip('\n') for user in File_Obj.readlines()]

Counter = 0
WaitTime = randint(200, 400)

# XPATH Vars
'''These variables are updatable, you can update them if these xpath doesn't work'''
# OLD # Follow_Button_XPATH = """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[2]/div/div[1]"""
# OLD # Three_Dots_XPATH = """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[3]/div/div"""
# OLD # Block_Button_XPATH = """/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/button[1]"""
# OLD # Block_Confirm_XPATH = """/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/button[1]"""
# OLD # Follow_Button_XPATH = '''/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section/div[1]/div[2]/div/div/button'''
# OLD # Three_Dots_XPATH = '''/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section/div[1]/div[3]/div'''

Search_Button_XPATH = """/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]"""
Three_Dots_XPATH = '''/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[2]/div/div/div[3]/div/div'''
Block_Button_XPATH = '''/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/button[1]'''
Follow_Button_XPATH = '''/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/section[2]/div/div/div[2]/div/div[1]'''
Block_Confirm_XPATH = '''/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/button[1]'''

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
    with open(f'{USERNAME}.txt', 'w') as File_Obj:
        [File_Obj.write(element + '\n') for element in List]

def Retrive_Blocked_List():
    with open(f'{USERNAME}.txt', 'r') as File_Obj:
        Data = [element.strip('\n') for element in File_Obj.readlines()]
    return Data

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
    WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Three_Dots_XPATH)))
    RandWait()

    Follow_Button = Browser.find_element(By.XPATH, Follow_Button_XPATH)
    if str(Follow_Button.text) == "Unblock":
        RandWait()
        return None
    
    RandWait()
    
    Three_Dots = Browser.find_element(By.XPATH, Three_Dots_XPATH)
    Three_Dots.click()
    WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Block_Button_XPATH)))
    RandWait()
    
    Block_Button = Browser.find_element(By.XPATH, Block_Button_XPATH)
    Block_Button.click()
    WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Block_Confirm_XPATH)))
    RandWait()
    
    Block_Confirm = Browser.find_element(By.XPATH, Block_Confirm_XPATH)
    Block_Confirm.click()
    sleep(4)
        
    Browser.get(LINK)
    WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Search_Button_XPATH)))
    return True

# Vars
if Blocked_List_Exists:
    Blocked = Retrive_Blocked_List()
    To_Block = New_List()
    
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

print("Press 'Ctrl + c' to stop")

for User in To_Block:
    try:
        Val = Block(PROFILE.format(User))
        if Val == None:
            print(f"{User} Already Blocked")
            Blocked.append(User)
            Browser.get(LINK)
            WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Search_Button_XPATH)))
        elif Val == True:
            Blocked.append(User)
            Counter += 1
    
        try:
            if Flag:
                Flag = False
                Notification_Not_Now = Browser.find_element(By.CLASS_NAME, "_a9_1")
                Notification_Not_Now.click()
            RandWait()
        except Exception as Error:
            Flag = False
            RandWait()

        if Counter == 12:
            Counter = 0
            sleep(WaitTime)
    
    except KeyboardInterrupt:
        print("[Ctrl + c] recieved.. stopping now!!")
        New_Blocked_List(Blocked)
        quit()
    
    except Exception as Error:
        print(Error)
        try:
            Browser.get(LINK)
            WebDriverWait(Browser, 10).until(EC.presence_of_element_located((By.XPATH, Search_Button_XPATH)))
            RandWait()
        except Exception as Error_2:
            print(Error_2)
            New_Blocked_List(Blocked)
            quit()
            
    

#Quit
sleep(15)
Browser.quit()
New_Blocked_List(Blocked)