from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
import csv


def get_url(search_text):
    """Generate a url from search text"""
    url = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'.format(search_text)
    
    # add page query
    url += '&page{}'
        
    return url


def extract_record(single_record):
    """Extract and return data from a single record"""

    
    # Title
    title_tag = single_record.h2.a
    title = title_tag.text.strip()
    url = 'https://www.amazon.com' + title_tag.get('href')
    
    # because some products dont have prices we have to 
    # use try-except block to catch AttributeError
    try:
        # product price
        price_parent = single_record.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    result = (title, price)
    
    return result

def main(search_term):


    """Run main program routine"""
    
    # startup the webdriver
    options=Options()
    
    options.headless = False #choose if we want the web browser to be open when doing the crawling 
    # options.use_chromium = True
    driver = webdriver.Chrome('/home/muhammed/Desktop/dev/blog-repo/selenium-tutorial/chromedriver')

    records = []
    url = get_url(search_term)
    
    for page in range(1, 5):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    
    driver.close()
    
    print(records)


main("sneakers")