import time
import re

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
    for i in row.find_all('a'):
        if "Alıntılanma sayısı:" in i.text:
            return i.text
    return "0"

def find_title(row):
    h3_obj = row.find('h3', class_ = "gs_rt")
    title = ""
    if h3_obj:
        title = h3_obj.find('a').text.strip()
    return title

def find_authors(row):
    gs_ri = row.find('div', class_ = "gs_ri")
    if gs_ri:
        gs_a = gs_ri.find('div', class_='gs_a')
        if gs_a:
            authors = gs_a.find_all('a')
            if authors:
                author_list = []
                for i in authors:
                    author_list.append(i.text.strip())
                return author_list
            else:
                return [gs_a.text.strip().split('-')[0]]

def find_date(row):
    gs_ri = row.find('div', class_ = "gs_ri")
    if gs_ri:
        gs_a = gs_ri.find('div', class_='gs_a')
        if gs_a:
            for i in gs_a.text.strip().split('-'):
                match = re.search(r'\b\d{4}\b', str(i))
                if match:
                    # Extract the matched four-digit number
                    date = match.group()
                    return date

def find_p_type(row):
    # publication_type
    publication_type = ""
    span_element = row.find('span', class_='gs_ct1')
    if span_element:
        publication_type = span_element.text.strip()
    return publication_type

def find_publisher(row):
    gs_ri = row.find('div', class_ = "gs_ri")
    if gs_ri:
        gs_a = gs_ri.find('div', class_='gs_a')
        if gs_a:
            return gs_a.text.strip().split('-')[-1]

def find_keywords_article(row):
    word_list = []
    gs_ri = row.find('div', class_ = "gs_ri")
    if gs_ri:
        gs_rs = gs_ri.find('div', class_='gs_rs')
        if gs_rs:
            for word in gs_rs.find_all('b'):
                if word not in word_list:
                    word_list.append(word)
            return word_list

def find_url(row):
    h3_obj = row.find('h3', class_ = "gs_rt")
    url = ""
    if h3_obj:
        url = h3_obj.find('a')["href"]
    return url

def scrape_website(parameter):
    #writedataToFile()
    scrappedData = {"publications": []}

    data = readDataFromFile()

    rows = get_rows(data)
    publications = scrappedData.get("publications", [])
    counter = 0
    for row in rows:
        counter += 1

        title = find_title(row)
        print("title : ", title)

        authors = find_authors(row)
        print("authors : ",authors)

        publication_type = find_p_type(row)

        date = find_date(row)
        print("date : ", date)

        publisher = find_publisher(row)
        print("publisher : ", publisher)

        parameter_string = str(parameter)
        print("keywords_search", parameter_string.split(' '))
        keywords_search = parameter_string.split(' ')

        keywords_article = find_keywords_article(row)
        print("keywords_article : ", keywords_article)

        p_url = find_url(row)
        print("find_url : ", p_url)

        #citation_count
        citation_count = 0
        citation_count = int(get_alinti(row).split(":")[1].strip())

        new_publication = {
            "title": title,
            "authors": authors,
            "publication_type": publication_type,
            "publication_date": date,
            "publisher": publisher,
            "keywords_search": keywords_search,
            "keywords_article": keywords_article,
            "abstract": "New Abstract of the publication.",
            "references": ["New Reference 1", "New Reference 2"],
            "citation_count": citation_count,  # Set initial citation count to 0
            "doi": "New DOI Number",
            "url": p_url
        }
        publications.append(new_publication)

    # Placeholder function. Replace it with your actual web scraping code.
    card_data_list = [
        {'title': 'Card 1', 'description': 'This is the first card.', 'url': '/link-to-card-1/'},
        {'title': 'Card 2', 'description': 'This is the second card.', 'url': '/link-to-card-2/'},
        {'title': 'Card 3', 'description': 'This is the third card.', 'url': '/link-to-card-3/'},
        # Add more cards as needed
    ]
    return card_data_list