import requests
import csv
import os
from bs4 import BeautifulSoup

INPUT_CSV = "./pico8-carts_5_24_22_FeaturedCarts.csv"
#INPUT_CSV = "./test.csv"
CART_FOLDER = "./result/Carts/"
RES_CSV = "./result/dataset.csv"
                
def main():
    with open(INPUT_CSV) as csvFile:
        print("Opening "+ RES_CSV)
        with open(RES_CSV, 'w', newline='') as resultFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            csvWriter = csv.writer(resultFile, delimiter=',')
            headers = next(csvReader)
            headers.append("License,Description,FileName")
            csvWriter.writerow(headers)
            
            for entry in csvReader:
                link = entry[4]
                res = requests.get(link)
                soup = BeautifulSoup(res.content, 'html.parser')
                assert(res.status_code == 200)

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
                    description += i.text + " "
                #Get rid of last newline
                description = description[:-1]

                #Handle Cart
                #Turn into p8, then get code and make lua copy
                fileName = ''.join(filter(str.isalpha, entry[3]))
                soupRes = soup.find_all(string="Cart")
                pngFile = requests.get("https://www.lexaloffle.com"+soupRes[0].parent['href']) 
                with open("./result/png/"+fileName+".p8.png", 'wb') as f:
                    f.write(pngFile.content)
                #Now convert .p8.png to .p8

                #Now extract code from .p8 to .lua file

                #Write new csv entry
                csvWriter.writerow(entry+[license, description, fileName])
                os.system("python3 ./shrinko8/shrinko8.py ./result/png/"+fileName+".p8.png ./result/p8/"+fileName+".p8")
                os.system("python3 ./shrinko8/shrinko8.py ./result/png/"+fileName+".p8.png ./result/lua/"+fileName+".lua")


main()     