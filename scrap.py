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
            csvWriter = csv.writer(resultFile, delimiter=',')

            for link in [ "https://www.lexaloffle.com/bbs/?tid=2145" ,"https://www.lexaloffle.com/bbs/?tid=36053"]:
                print(link)
                res = requests.get(link)
                soup = BeautifulSoup(res.content, 'html.parser')
                soupRes = soup.find_all(string="License:")    
                if len(soupRes) > 0:
                    resParent = soupRes[0].parent
                    print(resParent.next_sibling.next_sibling.text)
                else:
                    soupRes = soup.find_all(string="No License")
                    if len(soupRes) > 0:
                        print(soupRes)
main()     