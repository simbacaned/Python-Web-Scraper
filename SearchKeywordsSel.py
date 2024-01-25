from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import os
import re

columns = ["Website Address", "Website Name", "Site Rating", "Raw # Wealth Words",
           "% Wealth Words", "Raw # Health Words", "% Health Words",
           "Raw # Relationship Words", "% Relationship Words"]

keywords = [
    ["wealth", "money", "profit", "monetization", "property", "price", "drop ship", "yield", "cost", "business", "market", "pricing", "capital", "cash", "consumer", "expenditure", "supply", "demand", "economic", "value", "hedging", "income", "inflation", "tax", "liquidity", "monopoly", "mortgage", "oligopoly"],
    ["health", "mental", "body", "wellness", "emotional", "physical", "spiritual", "clinic", "care", "psychiatric", "livewell", "lifestyle", "illness", "behavior", "gym", "fitness", "pilates", "workout", "diet", "aerobic", "nutrition", "weight", "run", "swim", "jog", "athletic", "in shape", "detox", "sleep", "stress"],
    ["relationship", "friend", "respect", "safety", "equality", "love", "client", "family", "marriage", "rapport", "cooperation", "collaboration", "trust", "communication", "intimacy", "vulnerability", "reliance", "romance", "peace", "network", "platonic", "codependent", "support", "group", "interact", "feedback"]]

if not os.path.isdir("csv"):
    os.mkdir("csv")
    
csvFile = open("csv\\myCSV.csv", "a+", encoding="utf-8")
csvFileRead = open("csv\\myCSV.csv", "r", encoding="utf-8")

csvText = csvFileRead.read()
if csvText.split("\n")[0].split(",")[0] == "Website Address":
    print("File Written To Already")
if csvText.split("\n")[0].split(",")[0] != "Website Address":
    for column in columns:
        csvFile.write(column + ",")
    csvFile.write("\n")

urlFile = open("testURLs.txt", "r")
myURLs = urlFile.read().split("\n")

def CheckKeywords(mySoup, writeURL, writeRating):
    # Get all the text within the <body> element
    body_text = mySoup.body.get_text()
    writeTitle = mySoup.title.get_text().replace(",","").replace("\n","").replace("\t","")
    # Use re.findall to find and print the sentences containing the word
    catWords = [0,0,0]

    for i in range(0,3):
                for word in keywords[i]:
                    results = re.findall(word, body_text, re.I)
                    catWords[i] += len(results)

    rawWords = catWords[0] + catWords[1] + catWords[2]
    
    if rawWords != 0:
        print ("For website : " + writeTitle + " : " + writeURL)
        print ('Found {0} wealth words'.format(catWords[0]))
        print ('Found {0} health words'.format(catWords[1]))
        print ('Found {0} relationship words\n'.format(catWords[2]))    
        csvFile.write(writeURL + ",")
        csvFile.write(writeTitle + ",")
        csvFile.write(writeRating + ",")
        csvFile.write(str(catWords[0]) + ",")
        csvFile.write(str(100 * catWords[0]/rawWords) + "%,")
        csvFile.write(str(catWords[1]) + ",")
        csvFile.write(str(100 * catWords[1]/rawWords) + "%,")
        csvFile.write(str(catWords[2]) + ",")
        csvFile.write(str(100 * catWords[2]/rawWords) + "%,")
        csvFile.write("\n")
    else:
        print("Found zero key words : Skipping\n")

def CheckTitle(titleText):
    if titleText[3:] == "ClickFunnels™ - Marketing Funnels Made Easy":
        print("Website Expired : Skipping\n")
        return False
    elif titleText == "404 error page":
        print("404 Error : Skipping")
        return False
    else:
        return True
            
def OpenPage(currentRow):

    currentURL = "http://www." +  currentRow.split(",")[0]
    try:
        #Open Webpage
        driver.get(currentURL)

        #Get raw HTML
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        
        titleText = soup.title.get_text()

        if titleText == "CNAME Cross-User Banned | Cloudflare" or titleText == "404 error page" or titleText == "Privacy error":
            currentURL = currentURL[0:7] + currentURL[11:len(currentURL)]
            driver.get(currentURL)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            titleText = soup.title.get_text()
            if titleText == "Privacy error":
                raise Exception("Privacy error")
                
                    
        if CheckTitle(titleText):
            websiteRating = currentRow.split(",")[1]
            CheckKeywords(soup, currentURL, websiteRating)

            
    except WebDriverException:
        try:
            currentURL = currentURL[0:7] + currentURL[11:len(currentURL)]
            driver.get(currentURL)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            titleText = soup.title.get_text()
            
            if CheckTitle(titleText):
                websiteRating = currentRow.split(",")[1]
                CheckKeywords(soup, currentURL, websiteRating)            
        except Exception as e:
            print(e)
            print("Webpage Failed to Load : Skipping\n")
    except AttributeError:
        print(currentURL + " Has no Body : Skipping\n")
    except Exception as e:
        print(e)


for row in myURLs:
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service = service, options = options)
    OpenPage(row)

driver.quit()
csvFile.close()
urlFile.close()
csvFileRead.close()

input()
