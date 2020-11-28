from selenium import webdriver
from bs4 import BeautifulSoup 
import csv

def get_url(search):
    """ generates a url from search tearm """
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2"
    search = search.replace(" ", "+")
    
    #add search term to the URL
    url = template.format(search)
    
    #add page quary placeholder
    url += '&page={}'
    
    return url

def extract_data(item):
    """ Extract and return the data of the item"""
    atag = item.h2.a
    item_url = "https://amazon.com" + atag.get('href')
   
    #name
    item_name = atag.text.strip()
    try:
        #price
        price_parent = item.find('span', 'a-price')
        item_price= price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    
    try:
        #reviews
        item_rating = item.i.text
        item_rating_amount = item.find('span', {'class':'a-size-base', 'dir':'auto'}).text
    except AttributeError:
        item_rating = ''
        item_rating_amount = ''

    return (item_name, item_url, item_price, item_rating, item_rating_amount)

def main(search):
    """ Run main program runtime """
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    
    records = []
    url = get_url(search)
    driver.get(url)
    for page in range(1,21):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for result in results:
            record = extract_data(result)
            if record:
                records.append(record)
    
    driver.close()
    
    with open("{}".format(search)+".csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', "URL", "Price", 'Rating', 'Amount of Reviews'])
        writer.writerows(records)

main("Cycling Jersey Men")