import requests
import sys
import traceback
import time
from random import choice
from bs4 import BeautifulSoup
from bs4 import NavigableString
from urlparse import urljoin
import csv
from multiprocessing import Pool
import multiprocessing
import copy
import re
import os
import time
from threading import Timer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.common.exceptions import TimeoutException
import smtplib
import email


reload(sys)  
sys.setdefaultencoding('utf8')

LIMIT_TIME = 90
GAP = 0
DELAY = 10

  
def SendEmailWithGmail(TEXT):
    gmail_user = "stevehunter946@gmail.com"
    gmail_pwd = "mrpgm124"
    TO = 'mrpgm124@gmail.com'
    SUBJECT = "Testing sending using gmail"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    BODY = '\r\n'.join(['To: %s' % TO,
        'From: %s' % gmail_user,
        'Subject: %s' % SUBJECT,
        '', TEXT])

    server.sendmail(gmail_user, [TO], BODY)

def crawl ():

    SoccorDict = {}

    driver.get("https://www.bet365.com/en/")

    driver.add_cookie({'name':'aps03', 'value':'oty=1&cg=0&cst=119&tzi=27&hd=N&lng=1&cf=N&ct=42'})
    driver.add_cookie({'name':'rmbs', 'value':'3'})
    driver.get("https://www.bet365.com/#/IP/")

    while True:
        src = driver.page_source 
        soup = BeautifulSoup(src,"lxml") 

        Bar_Labels = soup.find_all("div", class_="ipo-ClassificationBarButtonBase_Label ")
        QuickBet = soup.find("div", class_="qb-Btn_Text-quick")
        
        if Bar_Labels:
            SoccerTitle = soup.find("div", class_="ipo-ClassificationHeader_HeaderLabel ")

            driver.find_element_by_xpath("//div[@class='ip-DropDownContainer_Button ipo-InPlayClassificationMarketSelectorDropDown_Button ipo-InPlayClassificationMarketSelectorDropDown_Button-1 ']").click()

            time.sleep(1.2)

            DropDownItems = driver.find_elements_by_xpath("//div[@class='ipo-InPlayClassificationMarketSelectorDropDown_DropDownItem ipo-MarketSelectorDropDownItem wl-DropDownItem ']")
            DropDownItems[1].click()           

            time.sleep(3)

            break
           
        time.sleep(1)

    while True:
        src = driver.page_source
        soup = BeautifulSoup(src,"lxml")

        Leagues = soup.find_all("div", class_="ipo-Competition ipo-Competition-open ")
        for League in Leagues: 
            
            NewDict = {}
            Matches = League.find_all("div", class_="ipo-Fixture_TableRow ")
        
            for Match in Matches:
                SoccerTime = Match.find("div", class_="ipo-InPlayTimer ")
                SoccerTime_N = int(SoccerTime.text[:2])
                if SoccerTime_N < LIMIT_TIME:
                    BlackLen = len(Match.find_all("div", class_="ipo-MainMarketRenderer_BlankParticipant "))
                    if BlackLen != 9:
                        BlackLen += len(Match.find_all("div", class_="gl-ParticipantCentered ipo-AllMarketsParticipant gl-ParticipantCentered_BlankName gl-ParticipantCentered_Suspended "))
                        if BlackLen != 9:
                            continue

                    TeamWrapper = Match.find_all("span", class_="ipo-TeamStack_TeamWrapper")

                    if SoccorDict.get(TeamWrapper[0].text) != None:
                        if SoccerTime_N - SoccorDict[TeamWrapper[0].text] > GAP:
                            LeagueName = League.find("div", class_="ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading ")
                            Team1 = TeamWrapper[0].text + " : " +Match.find("div", class_="ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamone ").text
                            Team2 = TeamWrapper[1].text + " : " +Match.find("div", class_="ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamtwo ").text

                            message = '\r\n'.join(['%s\r\n' % LeagueName.text,
                                                   '%s  %s' % (SoccerTime.text, Team1),
                                                   '       %s' % Team2])

                            SendEmailWithGmail(message)
                            continue
                                                
                        NewDict[TeamWrapper[0].text] = SoccorDict[TeamWrapper[0].text]
                        continue

                    NewDict[TeamWrapper[0].text] = SoccerTime_N   

        SoccorDict = NewDict.copy()
        time.sleep(DELAY)

    return

if __name__ == '__main__':

    driver = webdriver.Firefox()
    crawl()
    driver.quit()
    