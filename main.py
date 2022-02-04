import io

import requests
from bs4 import BeautifulSoup

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

    r1 = session.get(authURL, headers=basicHeaders) # Initiate and assign BeautifulSoup
    findAuthCodeSoup = BeautifulSoup(r1.content, 'html.parser') # Scrape the Challonge page
    authToken = findAuthCodeSoup.find("input", type="hidden", attrs={"name": "authenticity_token"})['value'] # Scrape the auth code needed to log into the site

    payload = {
        'authenticity_token': authToken,
        'user_session[username_or_email]': mail,
        'user_session[password]': password,
        'user_session[remember_me]': 1,
        'commit': 'Log in'
    } # Payload needed to log into the website

    session.post(loginURL, headers=basicHeaders, data=payload, cookies=r1.cookies) # Post to the Request URL to log in
    print("Successfully logged in!\n")

    return session, authToken # Return session to keep cookies persistent

def registerUser(session, username, authToken, link, discordBot):
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
    tournamentPage = BeautifulSoup(r1.content, 'html.parser')

    tournamentRules = rules(tournamentPage, discordBot)

    scrapedScript = tournamentPage.findAll("script")[16].string
    print("Scraping subscription code...")
    subscription = scrapeSubCode(scrapedScript)
    #print("Found subscription code:", subscription + "\n")

    print("Checking if tournament is available and allowing signups...")
    checkAvail = session.post("https://challonge.com/tournaments/" + subscription +  "/participants/check_avail.json", headers=basicHeaders, json=availPayload)
    print("Availability:", checkAvail.status_code)

    if checkAvail.status_code == 200:
        print("Tournament available! Signing up...\n")
        register = session.post("https://challonge.com/tournaments/" + subscription + "/participants/register.json", headers=regHeaders, json=registerPayload)
        print("Registration:", register)
        if register.status_code == 201:
            print("Registration complete! Good luck on the tournament")
            return tournamentRules
        else:
            print("Error! Something went wrong along the way. Please message Deviance#3806 for any bugs or double check the tournament/login details")
            return
    else:
        print("Tournament not available. Please message the TO for help")
        return

def checkIn(session, username, authToken, link):
    regHeaders = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Host": "challonge.com",
                "Origin": "https://challonge.com",
                "Referer": "https://challonge.com/tournaments/signup/jUKPpXcRse",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

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

    tournamentPage = findSubCodeSoup.findAll("script")[16].string
    print("Scraping subscription code...")
    subscription = scrapeSubCode(tournamentPage)
    print("Found subscription code:", subscription + "\n")

    print("Tournament available! Checking in...\n")
    checkingIn = session.post("https://challonge.com/tournaments/" + subscription + "/participants/163586547/check_in", headers=regHeaders, data=registerPayload)
    print("Check-in:", checkingIn.status_code)
    if checkingIn.status_code == 201:
        print("Check-in complete! Good luck on the tournament")
        return
    else:
        print("Error! Something went wrong along the way. Please message Deviance#3806 for any bugs or double check the tournament/login details")

def unregister(session, authToken, link):
    unregLink = link + "/participant_settings"
    unregHeaders = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded",
                "dnt": "1",
                "Host": "challonge.com",
                "Origin": "https://challonge.com",
                "Referer": unregLink,
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

    unregisterPayload = {
        "_method": "delete",
        "authenticity_token": authToken
    } # Payload needed to unregister

    print("Going to unregister page...")
    r1 = session.get(unregLink, headers=basicHeaders)
    print("Scraping unregister page...\n")
    scrapedUnregisterLink = BeautifulSoup(r1.content, 'html.parser')

    scrapedUnregisterLink = scrapedUnregisterLink.find(class_='btn btn-danger btn-sm pull-right', href=True)
    scrapedUnregisterLink = scrapedUnregisterLink['href']

    scrapedUnregisterLink = "https://challonge.com" + scrapedUnregisterLink
    print("Unregister link:", scrapedUnregisterLink)

    print("Tournament available! Unregistering...\n")
    unregister = session.post(scrapedUnregisterLink, headers=unregHeaders, data=unregisterPayload)
    print("Unregister status code:", unregister)

    if unregister.status_code == 302 or unregister.status_code == 200: # Returns code 200 even though normally it is supposed to return 302, it still unregisters the user, so we can pass it as successful
        print("Check-in complete! Good luck on the tournament")
        return
    else:
        print("Error! Something went wrong along the way. Please message Deviance#3806 for any bugs or double check the tournament/login details")

def rules(tournamentPage, discordBot):
    # class with rules is "tournament-description limited_width"
    tournamentRules = tournamentPage.find(class_="tournament-description limited_width")
    tournamentRulesFormatted = tournamentRules.get_text('\n', strip=True)
    tournamentRulesFormatted = tournamentRulesFormatted.replace('Show Full Description', '')

    if not discordBot:
        print("Rules:\n\n" + tournamentRulesFormatted)
        choice = input("\nDo you agree to the rules? [Y] or [N]: ")
        if choice == "Y" or choice == "y":
            return
        else:
            print("Since you do not agree, you will not be able to sign up to the tournament.")
            quit()
    else:
        return tournamentRulesFormatted
    return

def scrapeSubCode(scrapedScript):
    f = io.StringIO(scrapedScript) # Read variable as a text file by streaming it as an IOStream
    subscription = f.readlines()[4] # Go to the specific line which contains the subscription code

    subscription = subscription.replace("\n", "")
    subscription = subscription.replace("var subscription = client.subscribe('/tournaments/", "")
    subscription = subscription.replace("', function(message) {", "")
    subscription = subscription.replace(" ", "")
    # REALLY ugly way to get the subscription code to sign up, I will think of a better solution soon
    subscription = subscription

    return subscription

def main():
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
    print("")
    choice = input("""
    [1] Register
    [2] Check-in (WIP)
    [3] Unregister
    [4] Quit Program
    """)

    if choice == "1":
        challongeLink = input("Please input the challonge link for registering: ")
        loginDetails = getLoginDetails("login.txt")
        session, authToken = login(loginDetails[0], loginDetails[1], False)
        registerUser(session, loginDetails[2], authToken, challongeLink, False)
        input("Press [ENTER] to exit program...")
        quit()

    elif choice == "2":
        challongeLink = input("Please input the challonge link for check-in: ")
        loginDetails = getLoginDetails("login.txt")
        session, authToken = login(loginDetails[0], loginDetails[1], False)
        checkIn(session, loginDetails[2], authToken, challongeLink)
        input("Press [ENTER] to exit program...")
        quit()

    elif choice == "3":
        challongeLink = input("Please input the challonge link for unregistering: ")
        loginDetails = getLoginDetails("login.txt")
        session, authToken = login(loginDetails[0], loginDetails[1], False)
        unregister(session, authToken, challongeLink)
        input("Press [ENTER] to exit program...")
        quit()

    else:
        print("Quitting program...")
        quit()

#main() #Uncomment if wanting to use as standalone




