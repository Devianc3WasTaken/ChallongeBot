import io
import re
import time

from bs4 import BeautifulSoup
import requests
import pickle
import json
from datetime import datetime

#Challonge saves cookies for 3 months, requires re-login every 3 months

basicHeaders = {"Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}


def getLoginDetails(file):
    print("Getting login details...")
    loginDetails = ""
    with open(file) as f:
        line = f.read()
        line = line.strip()
        loginDetails = line.split(':')
    print("Found login details!\n")
    return loginDetails

def login(mail, password, expiredCookies):
    session = requests.Session() # Creating a Challonge session
    authURL = "https://challonge.com/user_session/new" # URL for acquiring auth code
    loginURL = "https://challonge.com/user_session?continue=%2F" # URL for logging in


    # Headers needed to access site, will give an 'Error 400' if not used

    r1 = session.get(authURL, headers=basicHeaders) # Initiate and assign BeautifulSoup
    findAuthCodeSoup = BeautifulSoup(r1.content, 'html.parser') # Scrape the Challonge page
    authToken = findAuthCodeSoup.find("input", type="hidden", attrs={"name": "authenticity_token"})['value'] # Scrape the auth code needed to log into the site
    
    print("Auth token for this session:", authToken + "\n")

    payload = {
        'authenticity_token': authToken,
        'user_session[username_or_email]': mail,
        'user_session[password]': password,
        'user_session[remember_me]': 1,
        'commit': 'Log in'
    } # Payload needed to log into the website

    #print("Logging in...")
    session.post(loginURL, headers=basicHeaders, data=payload, cookies=r1.cookies) # Post to the Request URL to log in
    '''#print("Successfully logged in!\n")
    
    with open('userCookies', 'wb') as f: # Saving cookies for future reference
        print("Saving cookies...")
        pickle.dump(session.cookies, f)

    print("Saved cookies!\n")'''

    return session, authToken # Return session to keep cookies persistent

def signup(session, username, authToken, link):
    regHeaders = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Host": "challonge.com",
                "Origin": "https://challonge.com",
                "Referer": "https://challonge.com/tournaments/signup/jUKPpXcRse",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

    availPayload = {
        'authenticity_token': authToken,
        'participant': {
                "name" : username
            }
    }  # Payload needed to check avail

    registerPayload = {
        "authenticity_token":authToken,
        "participant":{
            "name":username
        },
        "team":{
        }
    } # Payload needed to register


    print("Going to tournament page...")
    r1 = session.get(link, headers=basicHeaders)
    print("Scraping tournament page...\n")
    findSubCodeSoup = BeautifulSoup(r1.content, 'html.parser')
    # print(findSubCodeSoup.prettify())
    # time.sleep(1000)

    scrapedScript = findSubCodeSoup.findAll("script")[16].string
    print("Scraping subscription code...")
    subscription = scrape(scrapedScript)
    print("Found subscription code:", subscription + "\n")



    print("Checking if tournament is available and allowing signups...")
    checkAvail = session.post("https://challonge.com/tournaments/" + subscription +  "/participants/check_avail.json", headers=basicHeaders, json=availPayload)
    print("Availability:", checkAvail.status_code)

    if checkAvail.status_code == 200:
        print("Tournament available! Signing up...\n")
        register = session.post("https://challonge.com/tournaments/" + subscription + "/participants/register.json", headers=regHeaders, json=registerPayload)
        print("Registration:", register)
        if register.status_code == 201:
            print("Registration complete! Good luck on the tournament")
            return
        else:
            print("Error! Something went wrong along the way. Please message Deviance#3806 for any bugs or double check the tournament/login details")
            return
    else:
        print("Tournament not available. Please message the TO for help")
        return

def scrape(scrapedScript):
    f = io.StringIO(scrapedScript) # Read variable as a text file by streaming it as an IOStream
    subscription = f.readlines()[4] # Go to the specific line which contains the subscription code

    subscription = subscription.replace("\n", "")
    subscription = subscription.replace("var subscription = client.subscribe('/tournaments/", "")
    subscription = subscription.replace("', function(message) {", "")
    subscription = subscription.replace(" ", "")
    # REALLY ugly way to get the subscription code to sign up, I will think of a better solution soon
    subscription = subscription

    return subscription

print("""
  /$$$$$$ /$$               /$$/$$                                           /$$$$$$$            /$$    
 /$$__  $| $$              | $| $$                                          | $$__  $$          | $$    
| $$  \__| $$$$$$$  /$$$$$$| $| $$ /$$$$$$ /$$$$$$$  /$$$$$$  /$$$$$$       | $$  \ $$ /$$$$$$ /$$$$$$  
| $$     | $$__  $$|____  $| $| $$/$$__  $| $$__  $$/$$__  $$/$$__  $$      | $$$$$$$ /$$__  $|_  $$_/  
| $$     | $$  \ $$ /$$$$$$| $| $| $$  \ $| $$  \ $| $$  \ $| $$$$$$$$      | $$__  $| $$  \ $$ | $$    
| $$    $| $$  | $$/$$__  $| $| $| $$  | $| $$  | $| $$  | $| $$_____/      | $$  \ $| $$  | $$ | $$ /$$
|  $$$$$$| $$  | $|  $$$$$$| $| $|  $$$$$$| $$  | $|  $$$$$$|  $$$$$$$      | $$$$$$$|  $$$$$$/ |  $$$$/
 \______/|__/  |__/\_______|__|__/\______/|__/  |__/\____  $$\_______/      |_______/ \______/   \___/  
                                                    /$$  \ $$                                           
                                                   |  $$$$$$/                                           
                                                    \______/                  Made by Deviance#3806     
""")
print("\n\n")
challongeLink = input("Please input the challonge link: ")

loginDetails = getLoginDetails("login.txt")
session, authToken = login(loginDetails[0], loginDetails[1], False)
signup(session, loginDetails[2], authToken, challongeLink)
input("Press [ENTER] to exit program...")


