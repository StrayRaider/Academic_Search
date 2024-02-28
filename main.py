import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def getData():
    searchingText = "machine+learning"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
        response = requests.get('https://scholar.google.com/scholar',
                params={'hl' : 'tr', 'as_sdt' :'0%2C5', 'q': searchingText, 'btnG' : ''},
                headers=headers
            )
    except requests.exceptions.RequestException as error:
        print(f'An error occurred: {error}')
        return

    status_code = response.status_code
    print("Status code:", status_code)

    # If the status code is 200 (OK), print the first 500 characters of the HTML content
    if status_code == 200:
        #html_content = response.text
        #print(html_content)
        r = response

        soup = BeautifulSoup(r.content, 'lxml') 
        # printing our web page 

        #print(soup.prettify()) 



        # scrapping the links:- 

        # For all the 'href' links 

        #web_links = soup.select('a') 

        #actual_web_links = [web_link['href'] for web_link in web_links] 

        #print(actual_web_links)
        
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with id "gs_res_ccl_mid"
        #target_div = soup.find('div', id='gs_res_ccl_mid')
        target_div = soup.find('div')
        print(target_div.text,"\n")

        if target_div:
            print("Found div with id 'gs_res_ccl_mid':", target_div.text)
        else:
            print("Div with id 'gs_res_ccl_mid' not found.")
            

#getData()   


def writedataToFile():
    searchingText = "machine+learning"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
        response = requests.get('https://scholar.google.com/scholar',
                params={'hl' : 'tr', 'as_sdt' :'0%2C5', 'q': searchingText, 'btnG' : ''},
                headers=headers
            )
    except requests.exceptions.RequestException as error:
        print(f'An error occurred: {error}')
        return
    status_code = response.status_code
    print("Status code:", status_code)

    if status_code == 200:
        file = open("webPage.txt", "w")
        file.write(response.text)
        file.close()
        
def readDataFromFile():
    with open("webPage.txt", "r", encoding="utf-8") as file:
    # Reading form a file
        #print(file.read())
        return file.read()

def parseData(data):
    try:
        soup = BeautifulSoup(data, 'lxml')
        #print(soup.prettify())
        # mid divs
        divs = soup.find('div', id="gs_res_ccl_mid")
        
        if divs:
            # dive into rows :
            rows = divs.find_all('div', class_ = "gs_r gs_or gs_scl")
            for row in rows:
                print(f"row : {row} \n\n\n")
                pdfData = row.find('div', class_ = "gs_ggs gs_fl")
                print("pdf data : ", pdfData,"\n")
                for link in pdfData.find_all('a'):
                
                    print("link = ", link.get('href'),"\n")
        
            #print("Found div with id 'gs_res_ccl_mid':", divs.text)
            #print("divs count : ", len(divs.find_all('div', class_ = "gs_r gs_or gs_scl")),"\n")
            #for div in divs:
                #print("\n here : ",div,"\n")
        else:
            print("Div with id 'gs_res_ccl_mid' not found.")
        

    except Exception as e:
        print("Error:", e)

#writedataToFile()   
data = readDataFromFile()

parseData(data)
