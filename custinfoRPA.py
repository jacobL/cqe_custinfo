from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import requests
import time
import pyautogui as pag
import pymysql
import json
from datetime import datetime, timedelta
import random

def advanced_search(keyword) :
    conn = pymysql.connect( host = host , port=port , user = user , passwd = passwd , db = db )          
    cur = conn.cursor() 
    
    url = 'https://www.google.com/advanced_search'  
    option = webdriver.ChromeOptions()
    option.add_argument("--start-maximized")
    #option.add_argument('headless') 
    driver = webdriver.Chrome(r"D:\chromedriver.exe",chrome_options=option) 
    #driver = webdriver.Chrome(r"D:\chromedriver.exe")
    time.sleep(random.randint(3,6))
    driver.get(url) 
    time.sleep(2)  
    #keywordIn = 'allintext:' # 關鍵字出現在內文中
    #keyword1 = keywordIn+'Huawei 手機 site:https://www.mobile01.com/'
    #keyword2 = '對比度 Gamma'
    #keyword2 = '對比度 Gamma Color+temperature 反應速度 IPS Contrast 色彩溫度 輸入延遲 TN 伽瑪曲線' 
    #keyword2 = 'Delta+E 色溫 Response+time VA 色彩偏差值 色彩準確性 Input+lag'

    # 1.含以下所有字詞
    keywordlist = 'allintext:Huawei 手機 '+keyword+' site:https://www.mobile01.com/'
    driver.find_element_by_name("as_q").click()
    driver.find_element_by_name("as_q").clear()
    driver.find_element_by_name("as_q").send_keys(keywordlist)

    """
    # 2.含以下任何字詞
    driver.find_element_by_name("as_oq").click()
    driver.find_element_by_name("as_oq").clear()
    driver.find_element_by_name("as_oq").send_keys(keyword2)
    """
    
    #3.上次更新
    driver.find_element_by_xpath("//*[@id='as_qdr_button']/div[2]").click()
    time.sleep(1)
    #pag.moveTo(700, 820,1) #過去 24 小時內
    pag.moveTo(700, 910,1) #過去一個月內
    time.sleep(1)
    pag.click()

    #4.關鍵字出現的位置
    #driver.find_element_by_xpath("//*[@id='as_occt_button']/div[2]").click()
    #time.sleep(1)
    #pag.moveTo(700, 850,1) 
    #time.sleep(1)
    #pag.click()

    #5.搜尋
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/form/div[5]/div[9]/div[2]/input').click() 
    
    time.sleep(random.randint(4,8))
    
    # url
    #//*[@id="rso"]/div[2]/div/div[1]/a    
    #//*[@id="rso"]/div[10]/div/div[1]/a
    #//*[@id="rso"]/div[3]/div/div[1]/a
    
    # title1
    #//*[@id="rso"]/div[1]/div/div[1]/a/h3
    #//*[@id="rso"]/div[2]/div/div[1]/a/h3
    #//*[@id="rso"]/div[3]/div/div[1]/a/h3
    
    #//*[@id="rso"]/div[1]/div/div[1]/a/h3
    
    # publishdate
    #//*[@id="rso"]/div[1]/div/div[2]/div/span/span
    #//*[@id="rso"]/div[3]/div/div[2]/div/span/span
    #//*[@id="rso"]/div[3]/div/div[2]/div/span/span
    # abstract
    #//*[@id="rso"]/div[1]/div/div[2]/div/span
    #//*[@id="rso"]/div[3]/div/div[2]/div/span
    # 頁數
    #//*[@id="xjs"]/div/table/tbody/tr/td[3]/a
    #//*[@id="xjs"]/div/table/tbody/tr/td[3]/a
    #//*[@id="xjs"]/div/table/tbody/tr/td[3]/a
    #//*[@id="xjs"]/div/table/tbody/tr/td[3]/a
    #//*[@id="xjs"]/div/table/tbody/tr/td[4]/a
    #print('keyword1:',keyword1)
    pageIndex = 1
    while pageIndex < 4 :        
        try :
            #driver.find_element_by_id("foot")
            print("  pageIndex=",pageIndex )
            count = 1
            while count<11 :                 
                try :
                    url=driver.find_element_by_xpath("//*[@id='rso']/div["+str(count)+"]/div/div[1]/a").get_attribute("href")            
                    print('count=', count,' , url:',url)
                    title1=driver.find_element_by_xpath("//*[@id='rso']/div["+str(count)+"]/div/div[1]/a/h3").text
                    print('count=', count,' , title1:',title1)
                    publishdate=driver.find_element_by_xpath("//*[@id='rso']/div["+str(count)+"]/div/div[2]/div/span/span").text
                    print('count=', count,' , publishdate:',publishdate)
                    if '前' in publishdate and '天' in publishdate :
                        days = int(publishdate.split(' ')[0])
                        print('days:',days)
                        publishdate = (datetime.today() - timedelta(hours=24*days, minutes=0)).strftime('%Y%m%d')
                        print('publishdate:',publishdate)
                    elif '前' in publishdate and '時' in publishdate :
                        hours = int(publishdate.split(' ')[0])
                        print('hours:',hours)
                        publishdate = (datetime.today() - timedelta(hours=hours, minutes=0)).strftime('%Y%m%d')
                        print('publishdate:',publishdate)
                    elif '前' in publishdate and '分' in publishdate :    
                        minutes = int(publishdate.split(' ')[0])
                        print('minutes:',minutes)
                        publishdate = (datetime.today() - timedelta(hours=0, minutes=minutes)).strftime('%Y%m%d')
                        print('publishdate:',publishdate)
                    else :
                        y = publishdate.split('年')[0]
                        m = '0' + publishdate.split('年')[1].split('月')[0] if int(publishdate.split('年')[1].split('月')[0]) < 10 else publishdate.split('年')[1].split('月')[0]
                        d = '0' + publishdate.split('年')[1].split('月')[1].split('日')[0] if int(publishdate.split('年')[1].split('月')[1].split('日')[0]) < 10 else publishdate.split('年')[1].split('月')[1].split('日')[0]
                        publishdate = y+m+d
                    
                    abstract=driver.find_element_by_xpath("//*[@id='rso']/div["+str(count)+"]/div/div[2]/div/span").text
                    print('count=', count,' , abstract:',abstract)
                    creationdate = datetime.fromtimestamp(round(time.time(), 0)).strftime('%Y-%m-%d %H:%M:%S')
                    abstract = abstract.split(" - ", 2)[1] 
                    print(count,'. ',web,' ',app,' ',company,' ',keyword,' ',title1,' ',abstract,' ',publishdate,' ',url,' ',creationdate)
                    cur.execute('insert ignore into news(web,app,company,keyword,title1,abstract,publishdate,url,creationdate)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(web,app,company,keyword,title1,abstract,publishdate,url,creationdate))                     
                    cur.execute('commit')
                #except :
                #    print("count=",count," not found")
                except Exception as e:
                    print(e)    
                count = count + 1
            cur.execute('commit')
            
            pageIndexTmp = pageIndex+2
            #print('click next page 1 ',pageIndexTmp)
            time.sleep(random.randint(10,20))
            driver.find_element_by_xpath("//*[@id='xjs']/div/table/tbody/tr/td["+str(pageIndexTmp)+"]/a").click()           
            time.sleep(3)         
            
        except Exception as e:
            print(e)
            print("pageIndex not found, pageIndex=",pageIndex)
            break
        pageIndex = pageIndex + 1  

        
host = '10.55.52.98' 
port=33060 
user = 'root' 
passwd = "1234"

"""
host = '127.0.0.1' 
port=3306 
user = 'root' 
passwd = "1234"
"""
db='custinfo'
keywordIn = 'allintext:' # 關鍵字出現在內文中

#keyword2 = '對比度 Gamma Color+temperature 反應速度 IPS Contrast 色彩溫度 輸入延遲 TN 伽瑪曲線' 
#keyword2 = 'Delta+E 色溫 Response+time VA 色彩偏差值 色彩準確性 Input+lag'
# 對比度 Gamma Color+temperature 反應速度 IPS Contrast 色彩溫度 輸入延遲 TN 伽瑪曲線 Delta+E 色溫 Response+time VA 色彩偏差值 色彩準確性 Input+lag
appList = ['手機']
companyList = ['Huawei','OPPO']

web = 'mobile01'
app = appList[0]
company = companyList[0]

#keywordList = ["對比度","Gamma","Color temperature","反應速度","IPS","Contrast","色彩溫度","輸入延遲","TN","伽瑪曲線","Delta E","色溫","Response time","VA","色彩偏差值","色彩準確性","Input lag"]
keywordList = ["Gamma","Color temperature","反應速度"]
for k in range(0,len(keywordList)) :    
    print(k,'. ',keywordList[k])
    #keyword = keywordIn+'Huawei 手機 '+keywordList[k]+' site:https://www.mobile01.com/'
    advanced_search(keywordList[k])
    time.sleep(random.randint(50,70))
    print('============================================================================')        