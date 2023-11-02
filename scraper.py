from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import webbrowser
import http.server
import socketserver

def get_page_content(link, next_page=False):
    try:
        driver = webdriver.Chrome()
        driver.get(link)

        next_page_link = None

        content = driver.page_source
        
        # retrieves a link to the next page
        if next_page == True:
            next_btn = driver.find_element(By.CSS_SELECTOR, '.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')
            next_page_link = next_btn.get_attribute('href')

        driver.quit()    
    
    except Exception:
        print('Error scraping link!') 
        exit(1) 

    else:      
        return content, next_page_link

def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    products = soup.find_all(class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v29yj4s4ehtz85288pxsajyojq0 s-latency-cf-section puis-card-border")

    items = {}
    skipped = 0
    for i, product in enumerate(products, start=1):
        # product title
        title = product.find('h2')
        
        try:
            # get product ratings
            ratings = product.find(class_='a-row a-size-small').find_all('span')
            ratings = (ratings[0].get('aria-label'), ratings[3].get('aria-label'))

            # get price
            price = product.find('span', class_='a-offscreen').text

            # get link to product
            link = f"https://www.amazon.com{title.find('a').get('href')}"

            # get image source
            img = product.find('img').get('src')
        
        except AttributeError:
            print(f'\nSkipped {title.text} because not all attributes have been found.')
            skipped += 1
            continue    

        items[i] = {'title' : title.text, 'price' : price, 'ratings': ratings, 'product_link' : link, 'img_src' : img}

    print(f"\nSuccess. {skipped} products have been skipped.")
    return items   

def format_data(data):
    with open(f'data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)     
        json_file.flush()


def main(link, pages):
    items = {}
    for i in range(pages):
        print(f" Now at page {i+1}")
        if i != pages -1:
            content, next_page = get_page_content(link, True)  
        else:
           content, next_page = get_page_content(link)   

        items.update(parse_page(content))
        link = next_page   

    format_data(items)
    
    print('\nScraped all pages. Opening server now...') 
    with socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler) as httpd: 
        webbrowser.open_new_tab('http://localhost:8000/index.html')
        httpd.serve_forever()


if __name__ == "__main__":
    link = input("Paste link here: ")
    if 'www.amazon.com' not in link:
        raise Exception("Please provide a valid amazon page link!")
    
    try:
        pages = int(input("Number of pages to scrape from (defaults to 1): "))
    except Exception:
        pages = 1    
    
    main(link, pages)
          