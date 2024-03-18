import time
import re
import os

import requests
import pymongo
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urlparse

import pymongo
from elasticsearch import Elasticsearch

def check_elasticsearch_connection(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Elasticsearch is connected and healthy
            print("Elasticsearch is connected and healthy.")
            return True
        else:
            # Elasticsearch responded with an error
            print("Elasticsearch responded with an error:", response.status_code)
            return False
    except requests.exceptions.RequestException as e:
        # Connection error occurred
        print("Error connecting to Elasticsearch:", e)
        return False

es = Elasticsearch(
    "http://localhost:9200"
)
es_url = "http://localhost:9200"

# Check Elasticsearch connection
is_connected = check_elasticsearch_connection(es_url)
print("Is Elasticsearch connected:", is_connected)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['publications']
collection = db['searcheds']
        
def readDataFromFile():
    with open("webPage.txt", "r", encoding="utf-8") as file:
        return file.read()

def getData(searchingText):
    print(searchingText)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
        response = requests.get(f'https://scholar.google.com/scholar?hl=tr&as_sdt=0%2C5&q={searchingText}&btnG=',
                headers=headers
            )
    except requests.exceptions.RequestException as error:
        print(f'An error occurred: {error}')
        return
    status_code = response.status_code
    print("Status code:", status_code)

    if status_code == 200:
        return response.text

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
    h3_obj = row.find('h3', class_ = "gs_rt")
    publication_type = ""
    if h3_obj:
        span_element = h3_obj.find('span', class_='gs_ct1')
        if span_element:
            publication_type = span_element.text.strip()
        else:
            publication_type = "[HTML][N]"
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
                if word.text.strip() not in word_list:
                    word_list.append(word.text.strip())
    return word_list

def find_url(row):
    h3_obj = row.find('h3', class_ = "gs_rt")
    url = ""
    if h3_obj:
        url = h3_obj.find('a')["href"]
    return url

def get_pdf(row):
    pdfData = row.find('div', class_ = "gs_ggs gs_fl")
    print("pdf data : ", pdfData,"\n")
    if pdfData:
        for link in pdfData.find_all('a'):
            print("link = ", link.get('href'),"\n")
            return link.get('href')

def getSite(url):
    try:
        timeout_value = (2, 2)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
        response = requests.get(url,
                headers=headers,timeout=timeout_value
            )
    except requests.exceptions.Timeout:
        print("The request timed out.")
        return
    except requests.exceptions.RequestException as error:
        print(f'An error occurred: {error}')
        return
    status_code = response.status_code
    print("Status code:", status_code)
    if status_code == 200:
        r = response
        soup = BeautifulSoup(r.content, 'lxml') 
        #print(soup.prettify()) 
        return soup

def springer_find_abstract(response):
    Abs_content = response.find('div', id="Abs1-content")
    if Abs_content:
        return Abs_content.text

def springer_find_ref(response):
    items_list = []
    ol_data = response.find('ol', class_="c-article-references")
    if ol_data:
        list_items = ol_data.find_all('li')
        items_list.extend([item.get_text(strip=True) for item in list_items])
    else:
        ul_data = response.find('ul', class_="c-article-references")
        if ul_data:
            list_items = ul_data.find_all('li')
            items_list.extend([item.get_text(strip=True) for item in list_items])
    return items_list

def iEEE_find_abstract(response):
    Abs_content = response.find('div', class_="abstract-text row g-0")
    if Abs_content:
        return Abs_content.text

def find_abstract_ref(publisher, p_url):
    publisher = publisher.replace(' ', '')
    if publisher == "Springer":
        response = getSite(p_url)
        if response:
            return [springer_find_abstract(response), springer_find_ref(response),find_DOI(response)]
    elif publisher == "ieeexplore.ieee.org":
        response = getSite(p_url)
        if response:
            return [iEEE_find_abstract(response), "", ""]
    elif publisher == "nature.com":
        response = getSite(p_url)
        if response:
            return [springer_find_abstract(response), springer_find_ref(response),find_DOI(response)]
    return ["","",""]

def find_DOI(response):
    # Find all <ul> elements with class "c-bibliographic-information__list"
    target_ul_elements = response.find('ul', class_=lambda classes: classes and 'c-bibliographic-information__list' in classes.split())
    dois = re.search(r'https://doi\.org/\S+', target_ul_elements.text.strip()).group()
    print("DOI Number : ", dois)
    return dois

def download_pdf(url):
    isPdf = url.split('.')[-1]
    name = url.split('.')[0]
    if isPdf == 'pdf':
        response = requests.get(url)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            with open(f'./pdfs/{os.path.basename(parsed_url.path)}', 'wb') as f:
                f.write(response.content)
    else:
        print("it is not pdf")

def find_Reference(url):
    return ["No Reference Founded"]

def writeToDb(publications):
    for publication in publications:
        url_to_check = publication.get("url")
        if url_to_check:
            existing_document = collection.find_one({"url": url_to_check})
            if existing_document:
                print(f"Document with URL '{url_to_check}' already exists. Skipping insertion.")
            else:
                # If the document with the URL doesn't exist, insert it
                collection.insert_one(publication)
                print(f"Inserted document with URL '{url_to_check}'.")
        else:
            print("URL not found in publication data. Skipping insertion.")


def findDoiFromUrl(url):
    # DOI'yi çıkarmak için regex deseni
    doi_pattern = r'\/(?P<doi>10\.\d{4,}\/[\w\.\-\/]+)'
    match = re.search(doi_pattern, url)
    if match:
        return match.group('doi')
    else:
        return None

def scrape_website(parameter):
    #writedataToFile()
    scrappedData = {"publications": []}

    #data = readDataFromFile()
    parameter = parameter.replace(' ', '+')
    data = getData(parameter)

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
        print("keywords_search", parameter_string.split('+'))
        keywords_search = parameter_string.split('+')

        keywords_article = find_keywords_article(row)
        print("keywords_article : ", keywords_article)

        p_url = find_url(row)
        print("find_url : ", p_url)

        abstract = " Not Found ! "
        site_data = find_abstract_ref(publisher, p_url)
        abstract = site_data[0]
        references = site_data[1]
        doi_num = site_data[2]
        #print("abstract : ",abstract)

        if doi_num == "":
            doi_num = findDoiFromUrl(p_url)

        pub_pdf = get_pdf(row)
        print("pdf : ", pub_pdf)

        #if pub_pdf:
        #    download_pdf(pub_pdf)

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
            "abstract": abstract,
            "references": references,
            "citation_count": citation_count,  # Set initial citation count to 0
            "doi": doi_num,
            "url": p_url,
            "pub_pdf":pub_pdf
        }
        publications.append(new_publication)
    writeToDb(publications)
    return publications


def get_searched():
    cursor = collection.find({})
    full_list = []
    for document in cursor:
        full_list.append(document)
    return full_list

def get_searched_sorted(key, direction):
    cursor = collection.find({}).sort(key, direction)
    full_list = []
    for document in cursor:
        full_list.append(document)
    return full_list

def get_searched_by_url(url_to_match):
    cursor = collection.find({"url": url_to_match})
    full_list = []
    for document in cursor:
        full_list.append(document)
    print(full_list)
    return full_list

def drop_col():
    collection.drop()


# Define a function to index documents into Elasticsearch
def index_documents(index_name, documents):
    # Connect to Elasticsearch

    # Iterate over each document and index it
    for doc_id, doc in enumerate(documents, start=1):
        # Index the document
        doc['_id'] = str(doc['_id'])
        
        # Convert non-ASCII characters to ASCII or Unicode
        doc['publication_type'] = doc['publication_type'].encode('ascii', 'ignore').decode('utf-8')
        
        # Index the document
        print("Document to be indexed:")
        print("Document to be indexed:")
        print(doc)
        es.index(index=index_name, body=doc, id=doc_id)

# Define a function to perform a filtered search
def filtered_search(index_name, field, value):
    # Connect to Elasticsearch

    # Define the search query with a filter
    search_query = {
        "query": {
            "match": {
                field: value  # Match documents where the specified field matches the given value
            }
        }
    }

    # Execute the search query
    search_results = es.search(index=index_name, body=search_query)

    # Extract the matching documents
    matching_documents = [hit["_source"] for hit in search_results["hits"]["hits"]]

    return matching_documents