
from bs4 import BeautifulSoup
from selenium import webdriver

# Google Chrome
driver = webdriver.Chrome('/home/muhammed/Desktop/dev/blog-repo/selenium-tutorial/chromedriver')



def get_url(search_text):
    """Generate a url from search text"""
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'.format(search_text)
    return template


url = get_url('sneakers')
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
record = soup.find_all('div', {'data-component-type': 's-search-result'})
single_record = record[0]
# print(single_record)



def extract_record(item):
    """Extract and return data from a single record"""
    
    # Title
    title_tag = single_record.h2.a
    title = title_tag.text.strip()
    url = 'https://www.amazon.com' + title_tag.get('href')
    
    # product price
    price_parent = single_record.find('span', 'a-price')
    price = price_parent.find('span', 'a-offscreen').text
    result = (title, price)
    
    return result


records = []

# get all search results
results = soup.find_all('div', {'data-component-type': 's-search-result'})

# extract data from each results
for item in results:
    records.append(extract_record(item))