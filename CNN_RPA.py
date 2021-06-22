from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import time
import pymysql
import random

def key_search(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver =webdriver.Chrome(r"D:\chromedriver.exe", chrome_options=options)
    wait = WebDriverWait(driver, 300)

    url = "https://edition.cnn.com/"
    driver.get(url)

    #click search button
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header-nav-container"]/div/div[1]/div/div[4]/button')))
    driver.find_element_by_xpath('//*[@id="header-nav-container"]/div/div[1]/div/div[4]/button').click()

    #enter the key
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header-search-bar"]')))
    driver.find_element_by_xpath('//*[@id="header-search-bar"]').send_keys(keyword)

    #search
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header-nav-container"]/div/div[2]/div/div[1]/form/button')))
    driver.find_element_by_xpath('//*[@id="header-nav-container"]/div/div[2]/div/div[1]/form/button').click()

    time.sleep(random.randint(3,6))

    #change type = article(Stories)
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/div/div[1]/div/div[3]/div[1]/ul/li[2]')))
    driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[1]/div/div[3]/div[1]/ul/li[2]').click()

    #change category = news
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="left_news"]')))
    driver.find_element_by_xpath('//*[@id="left_news"]').click()
   
    time.sleep(random.randint(10,20))
    isExpired = False
    while isExpired == False:
        try:
            count = 1
            while count<11 and isExpired == False:                 
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/h3'.format(count))))
                    title = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/h3'.format(count)).text

                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/h3/a'.format(count))))
                    element = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/h3/a'.format(count))
                    url = element.get_attribute('href')

                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/div[2]'.format(count))))
                    content = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/div[2]'.format(count)).text

                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/div[1]/span[2]'.format(count))))
                    date = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/div[1]/span[2]'.format(count)).text
                    print(date)


                    dates = date.split(' ')
                    dates[1].zfill(2)
                    date = ' '.join(dates)
                    dateFormatter = "%b %d, %Y"
                    publishdate = datetime.strptime(date, dateFormatter)


                    #抓取近一個月資料就好
                    difference = datetime.now() - publishdate
                    if difference.days > 30:
                        isExpired = True
                        break

                    creationdate = datetime.fromtimestamp(round(time.time(), 0)).strftime('%Y-%m-%d %H:%M:%S')
                    print(count,'. ',web,' ',app,' ',company,' ',keyword,' ',title,' ',content,' ',publishdate,' ',url,' ',creationdate)
                    # cur.execute('insert ignore into products(web,app,company,keyword,title1,title2,content,publishdate,url,creationdate)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(web,app,company,keyword,title,title,content,publishdate,url,creationdate))                     
                    # cur.execute('commit')
                except Exception as e:
                    print(e)

                count += 1

            if isExpired:
                break

            time.sleep(random.randint(10,20))

            # cur.execute('commit')
            #click next page
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[5]/div/div[3]')))
            driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[5]/div/div[3]').click()
        
        except Exception as e:
            print(e)
            break
        
        time.sleep(random.randint(60,80))
    driver.quit()



# host = '10.55.52.98'
# port = 33060
# user = 'root'
# passwd = "1234"

# db = 'custinfo'

# conn = pymysql.connect(host=host, port=port,
#                        user=user, passwd=passwd, db=db)
# cur = conn.cursor()
# cur.execute("select url from products where url like '%support/content%'")


# conn.commit()
# cur.close()
# conn.close()

web = 'CNN'
app = ''
company = ''

# keys = ['Huawei','Audi','Panasonic','Canon','Nintando'
# 'OPPO','Xiaomi','BMW','Alpine','Epson'
# 'Ricoh','Samsung','PSA ','DensoTen','Zebra'
# 'Amazon','GM','NS','Sony','vivo']
keys = ['19']

for key in keys:
    company = key
    key_search(key)

