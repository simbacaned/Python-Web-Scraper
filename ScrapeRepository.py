from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup
import os

torexe = os.popen(r'Browser\TorBrowser\Tor\tor.exe')
profile_path = r'Browser\TorBrowser\Data\Browser\profile.default'
options = Options()
options.set_preference("profile", profile_path)
options.set_preference("network.proxy.type", 1)
options.set_preference("network.proxy.socks", "127.0.0.1")
options.set_preference("network.proxy.socks_port", 9050)
options.set_preference("network.proxy.socks_remote_dns", False)

service = Service(executable_path=r"driver\geckodriver.exe")
driver = webdriver.Firefox(service = service, options = options)

now = datetime.now()
currentDateTime = now.strftime("%d_%m_%y-%H_%M_%S")
if not os.path.isdir("csv"):
    os.mkdir("csv")
f = open("csv\\urls" + currentDateTime + ".txt", "x")

def writeTotxt(rows):
    oddRow = 0
    for row in rows:
        print(row)
        if oddRow % 2 == 0:
            if row[1] == "www.":
                f.write(row[1][4:] + ",")
            else:
                f.write(row[1] + ",")
            f.write(row[5].replace(",","").replace("# ","") + ",")
        else:
            data = row[0].split("\n")
            datum = data[0]
            noVisitors = datum.replace(",","").replace("Website Popularity:","").replace(" visitors per day","")
            f.write(noVisitors)
            f.write("\n")
        oddRow += 1

def getInfoFromTable():
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', id='sites_tbl')
    rows = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 0:
            cols = row.find_all('th')
        cols = [ele.text.strip() for ele in cols]
        rows.append([ele for ele in cols if ele])
    onlyData = []
    for row in rows:
        if row[0] != "No":
            onlyData.append(row)
    writeTotxt(onlyData)

def getDataLoop(x,y,ip):
    for num in range(x,y + 1):
        url = "https://myip.ms/browse/sites/{0}/ipID/{1}/ipIDii/{1}".format(str(num), str(ip))
        driver.get(url)
        getInfoFromTable()
    f.close()

first = int(input("First page to read : "))
last = int(input("Last page to read from : "))
currentIP = str(input("The IP address you want to use : "))
getDataLoop(first, last, currentIP)
#34.68.234.4 - gohighlevel
#104.16.12.194 - clickfunnels
