from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

def get_page_content(link, next_page=False):
    driver = webdriver.Chrome()
    driver.get(link)

    next_page_link = None
    
    content = driver.page_source
    
    # retrieves a link to the next page
    if next_page == True:
        next_btn = driver.find_element(By.CSS_SELECTOR, '.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')
        next_page_link = next_btn.get_attribute('href')
    
    driver.quit()

    return content, next_page_link

def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    products = soup.find_all(class_="s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v20azwp0smsgc01ytmkntf1rk7n s-latency-cf-section s-card-border")

    items = {}
    skipped = 0
    for product in products:
        # product title
        title = product.find('h2')
        
        try:
            # get product ratings
            ratings = product.find(class_='a-row a-size-small').find_all('span')
            ratings = (ratings[0].get('aria-label'), ratings[3].get('aria-label'))

            # get price
            price = product.find('span', class_='a-offscreen').text

            # get link to product
            link = f"www.amazon.com{title.find('a').get('href')}"
        
        except AttributeError:
            print(f'Skipped {title.text} because not all attributes have been found.')
            skipped += 1
            continue    

        items[title.text] = {'price' : price, 'ratings': ratings, 'product_link' : link}

    print(f"success. {skipped} products have been skipped.")
    return items   

def format_data(data, page):
    with open(f'page_{page}.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)     


def main(link, pages):
    for i in range(pages):
        print(f" Now at page {i+1}")
        if i != pages -1:
            content, next_page = get_page_content(link, True)  
        else:
           content, next_page = get_page_content(link)   

        format_data(parse_page(content), i+1)
        link = next_page   

    print('Scraped all pages')  


if __name__ == "__main__":
    link = input("Paste link here: ")
    if 'www.amazon.com' not in link:
        raise Exception("Please provide a valid amazon page link!")
    
    try:
        pages = int(input("Number of pages to scrape from (defaults to 1): "))
    except Exception:
        pages = 1    
    
    main(link, pages)




       