# coding: utf-8

import os
import requests
import math
from bs4 import BeautifulSoup

import datetime
import random
from selenium import webdriver
import time

Tp = 3 #The total page number
#Sp = 1 #The start page number

#aidArray is used to stroe aids
aidArray = []

#you can download other upper's video by changing this parameter
upper_id = '10330740'

path = "./chromedriver.exe" #Get Chromedriver.exe path
driver = webdriver.Chrome(executable_path=path) #Drive Chrome
print('stage 1: obtain aids')
print('opening the chrmodriver...')


for page in range(1, Tp + 1) : #
    page_video = 0 #video index in current page
    print('opening page: ' + str(page))
    url = "https://space.bilibili.com/" + upper_id + "?from=search&seid=12264074931239145067#/video?tid=0&page=" + str(page) + "&keyword=&order=pubdate"
    #The homepage link for one upper whose uid is 10330740
    driver.get(url)
    #Load the url
    time.sleep(5)
    #Delay 5s

    while True : #Check out HTML entire page source codes for each page
        pageSourceThree = driver.page_source
        PageSourceHtml = BeautifulSoup(pageSourceThree,"html.parser")
        PageSourceBodyHtml = PageSourceHtml.find('ul', attrs={'class': 'list-list'})
        #Find out the information of all videos under lable '<ul> class = 'list-list' 
        if(str(PageSourceBodyHtml) == 'None'): #If that information cannot be obtain, delay 5s, return back and do again.
            time.sleep(5)
        else:
            detial = PageSourceBodyHtml.findAll('li', attrs = {'class':'list-item clearfix fakeDanmu-item'})
            #If got that information, find all videos' detials under lable <li> class = 'list-item clearfix fakeDanmu-item'
            if(str(detial) != '[]'): #If the detial is not empty, break the loop and start next page's work.
                break
            else: #If it is, sleep 5s
                time.sleep(5)
    #print(detial)

    #Sp = Sp + 1 #The current page number plus one.
    
    while True:
        try : #Find all aids from each page's HTML source codes
            aidStart = str(detial[page_video]).find('aid') + 5
            aidEnd = str(detial[page_video]).find('"><a') 
        
            #aidArray[j+30*(i-3)] = int(aid)
            #find the aid of this video
            aid = str(detial[page_video])[aidStart : aidEnd]
            aidArray.append(str(detial[page_video])[aidStart : aidEnd])
            print('found video number: ' + aid)
            page_video = page_video + 1
            time.sleep(0.5)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        except:
            #if all the video aids are already found, break and go to the next page
            break
    
    time.sleep(random.randrange(9))
    print('###############################################')


#######################################################################
#print(aidArray)
print('###############################################')
print('stage 2: download videos')

video_homepage = 'https://www.bilibili.com/video/av'
video_path = '.\\videos\\'

print('the videos will be saved in the path: ' + 'videos\')

for aid in aidArray:
    command = "lulu -o " + video_path + ' ' + video_homepage + aid
    #print(command)
    print("downloading video number: " + str(aid))
    starttime = datetime.datetime.now()
    os.system(command)
    endtime = datetime.datetime.now()
    print('finished videos ' + str(aidArray.index(aid)+1) + '/' + str(len(aidArray)))
    print('time spent: ' + str((endtime - starttime).seconds))
print('done!')