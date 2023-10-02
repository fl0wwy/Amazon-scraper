from selenium import webdriver
from bs4 import BeautifulSoup

def get_page_content(link):
    driver = webdriver.Chrome()
    driver.get("link")

    content = driver.page_source
    driver.quit()

    return content

def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    products = soup.find_all(class_="s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v20azwp0smsgc01ytmkntf1rk7n s-latency-cf-section s-card-border")

    items = {}
    for product in products:
        # product title
        title = product.find('h2').text
        
        try:
            # get product ratings
            ratings = product.find(class_='a-row a-size-small').find_all('span')
            ratings = (ratings[0].get('aria-label'), ratings[3].get('aria-label'))

            # get price
            price = product.find('span', class_='a-offscreen').text
        
        except AttributeError:
            print(f'Skipped {title} because not all attributes have been found.')
            continue    

        items[title] = {'price' : price, 'ratings': ratings}

    return items    

       