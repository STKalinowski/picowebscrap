import requests
import os
import csv
from io import StringIO
from bs4 import BeautifulSoup

from lxml import etree
import lxml



INPUT_CSV = "./pico8-carts_5_24_22_FeaturedCarts.csv"
CART_FOLDER = "./result/Carts/"
RES_CSV = "./result/dataset.csv"
                
def main():
    with open(INPUT_CSV) as csvFile:
        print("Opening "+ RES_CSV)
        with open(RES_CSV) as resultFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            headers = next(csvReader)
            headers.append("License,Description,FileName")
            csvWriter = csv.writer(resultFile, delimiter=',')

            for entry in csvReader:
                link = entry[4]
                res = requests.get(link)
                soup = BeautifulSoup(res.content, 'html.parser')
                print(link)

                #Handle Liscence
                soupRes = soup.find_all(string="License:")    
                if len(soupRes) > 0:
                    resParent = soupRes[0].parent
                    license = resParent.next_sibling.next_sibling.text
                else:
                    license = "No License"
                

                #Handle Descriptions
                description = ""
                soupRes = soup.select("#main_div > div:nth-child(5) > div:nth-child(1) > div > div > div:nth-child(2) > div:nth-child(3) > p")#.find_all("p")
                for i in soupRes[1:]:
                    description += i.text + "\n"
                #Get rid of last newline
                description = description[:-1]

                #Handle Cart
                #Turn into p8, then get code and make lua copy
                fileName = entry[3].strip()+".p8.png"
                soupRes = soup.find_all(string="Cart")
                pngFile = requests.get("https://www.lexaloffle.com"+soupRes[0].parent['href']) 
                with open("./png/"+fileName, 'wb') as f:
                    f.write(pngFile.content)
                break


main()     