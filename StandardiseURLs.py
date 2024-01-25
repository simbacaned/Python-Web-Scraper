import os
urlFile = open(r"urlList.txt", "r")
urls = urlFile.read()
urlList = urls.split("\n")
infoList = open(r"infoList.txt", "r")
infos = infoList.read()
info = infos.split("\n")

outPutFile = open(r"outputFile.txt","w+")


for url in urlList:
    for inf in info:
        newurl = url.replace("http://www.","")
        newurl = newurl.replace("https://www.","")
        newurl = newurl.replace("https://","")
        newurl = newurl.replace("http://","")
        if newurl == inf.split(",")[0]:
            outPutFile.write(inf.split(",")[2] + "\n")
            print(newurl, inf)
outPutFile.close()
