from bs4 import BeautifulSoup
import time
import requests
import urllib.request
import smtplib
import re
from IPython.display import clear_output

def getWords(URL):
    response = urllib.request.urlopen(URL).read()
    sitewords = response.decode("utf-8")
    return sitewords

def getSoup(URL):
    response = urllib.request.urlopen(URL)
    soup = BeautifulSoup(response, 'lxml')
    transactionSoup = soup.find_all('p', class_ = 'location')
    
    #return transactionSoup
    return soup


def sendEmail(content):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(GMAILusername, GMAILpassword)
    server.sendmail(fromAddress, toAdress, content)
    server.quit()
    print("Email sent!")
    return

    
    
#GMAILusername = input("Enter Gmail username (without @gmail.com): ")
#GMAILpassword = input("Enter Gmail password: ")

GMAILusername = ""
GMAILpassword = ""


fromAddress = GMAILusername + "@gmail.com"
toAdress = fromAddress


def mainUpdateCheck(URL, waitTime):
    siteChanged = False
    gotSiteContent = False
    tempWaitTime = 0
    while True:
        print("Refreshing website")
        while True:
            try:
                sitewords = getWords(URL)
            except Exception as e:
                print(e)
                continue
            break
        
        print("Got website data")
        
        location = sitewords.find("minutes ago")
        
        if location != -1: 
            timeString = sitewords[location - 16:location + 11]
            print(timeString)

            if ("hours" and "hour") not in timeString:
                print("RECENT PRINT DETECTED!")
                sendEmail("Tether printed!: " + timeString)

                tempWaitTime = 600
                print("Added 5 minutes to wait time")
            

        delay = waitTime + tempWaitTime
        print("Waiting {} minutes until next refresh.".format((delay) // 60))
        time.sleep(delay)
        tempWaitTime = 0
        clear_output(wait=True)
        
mainUpdateCheck("http://omnichest.info/lookupadd.aspx?address=3MbYQMMmSkC3AgWkj9FMo5LsPTW1zBTwXL", 300)


print("DONE")    

