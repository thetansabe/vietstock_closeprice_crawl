#libs
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime, timedelta

#variables
prefix = 'fpt' #change your stock here
prefix = prefix.upper()
url = f"https://finance.vietstock.vn/{prefix}/thong-ke-giao-dich.htm"

fromDate1 = "30/9/2022"
toDate1 = "10/11/2022"

fromDate2 = "11/11/2022"
toDate2 = "30/11/2022"

#open website
driver = webdriver.Chrome()
driver.get(url)

#pick date
def pickDate(driver, fromDate, toDate):
    fromDateInput = driver.find_element(By.NAME, "txtFromDate")
    fromDateInput.clear()
    fromDateInput.send_keys(fromDate)

    toDateInput = driver.find_element(By.NAME, "txtToDate")
    toDateInput.clear()
    toDateInput.send_keys(toDate)

    pageSizeInput = driver.find_element(By.NAME, "pageSize")
    pageSizeInput.clear()
    pageSizeInput.send_keys("30")

    sleep(1)
    xemBtn = driver.find_element(By.CSS_SELECTOR, 'button.btn.bg.m-l')
    xemBtn.click()

#convert string to currency
def fromStringToCurrency(s):
    return int(s.replace(',', ''))

#crawl from html
def getData(driver):
    data = []

    for count in range(1,35):
        try:
            tbody = driver.find_element(By.XPATH, f"//table[@class='table table-striped table-hover table-bordered m-b-xs']/tbody/tr[{count}]")
            strs = tbody.text.split(" ")
            dict = {'date': strs[0], 'close': fromStringToCurrency(strs[4])}
            data.append(dict)
        except Exception as e:
            print("error in for")
            break
    
    return data

#first get
pickDate(driver, fromDate2, toDate2)
data1 = getData(driver)
# print("data1: " + str(data1))

sleep(1)

#last get
pickDate(driver, fromDate1, toDate1)
data2 = getData(driver)
# print("data2: " + str(data2))

#merge data
data = data1 + data2
# print(data)
print("data len: " + str(len(data)))

# handle missing dates
def handleMissingDates(data, delta):
    tmp = data.copy()

    if(delta == 'sat'):
        wk_day = 4 #friday
    else:
        wk_day = 5 #saturday

    for dict in data:
        date_object = datetime.strptime(dict['date'], '%d/%m/%Y').date()
        
        if date_object.weekday() == wk_day:
            d = date_object + timedelta(days=1)
            tmp.insert(tmp.index(dict) + 1, {'date': d.strftime('%d/%m/%Y'), 'close': dict['close']})
    
    return tmp

#insert Sat and Sun
data.reverse()
dataWithSat = handleMissingDates(data, 'sat')
dataWithSun = handleMissingDates(dataWithSat, 'sun')

# to excel
try:
    tempCols = {'date': [dict['date'] for dict in dataWithSun],
                prefix: [dict['close'] for dict in dataWithSun]}
    newdf = pd.DataFrame(data=tempCols)
    newdf.to_excel(f'./sep_stock/{prefix}.xlsx', index=False)
    print('DONE')
except Exception as e:
    print("something wrong")
    print(e)