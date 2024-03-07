import time

import requests
import pymongo
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
        
def readDataFromFile():
    with open("webPage.txt", "r", encoding="utf-8") as file:
        return file.read()

def parseData(data):
    try:
        scrappedData = []
        soup = BeautifulSoup(data, 'lxml')
        #print(soup.prettify())
        # mid divs
        divs = soup.find('div', id="gs_res_ccl_mid")
        
        if divs:
            # dive into rows :
            rows = divs.find_all('div', class_ = "gs_r gs_or gs_scl")
            for row in rows:
                #print(f"row : {row} \n\n\n")
                pdfData = row.find('div', class_ = "gs_ggs gs_fl")
                print("pdf data : ", pdfData,"\n")
                scrappedData.append(pdfData)
                #for link in pdfData.find_all('a'):
                
                    #print("link = ", link.get('href'),"\n")
        
            #print("Found div with id 'gs_res_ccl_mid':", divs.text)
            #print("divs count : ", len(divs.find_all('div', class_ = "gs_r gs_or gs_scl")),"\n")
            #for div in divs:
                #print("\n here : ",div,"\n")
        else:
            print("Div with id 'gs_res_ccl_mid' not found.")
        

    except Exception as e:
        print("Error:", e)
    return rows

def get_rows(data):
    try:
        row_datas = []
        soup = BeautifulSoup(data, 'lxml')
        divs = soup.find('div', id="gs_res_ccl_mid")
        
        if divs:
            # dive into rows :
            rows = divs.find_all('div', class_ = "gs_r gs_or gs_scl")
            for row in rows:
                row_datas.append(row)
        else:
            print("Div with id 'gs_res_ccl_mid' not found.")
        
        return row_datas

    except Exception as e:
        print("Error:", e)

def get_alinti(row):
    return row.find_all('a', text='Alıntılanma sayısı:')

def scrape_website(param):
    #writedataToFile()   
    data = readDataFromFile()

    rows = get_rows(data)
    for row in rows:
        span_element = row.find('span', class_='gs_ct1')
        if span_element:
            print("Found span within div 'gs_ct1':", span_element.text)
        print(get_alinti(row))

    # Placeholder function. Replace it with your actual web scraping code.
    card_data_list = [
        {'title': 'Card 1', 'description': 'This is the first card.', 'url': '/link-to-card-1/'},
        {'title': 'Card 2', 'description': 'This is the second card.', 'url': '/link-to-card-2/'},
        {'title': 'Card 3', 'description': 'This is the third card.', 'url': '/link-to-card-3/'},
        # Add more cards as needed
    ]
    return card_data_list