from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from decimal import Decimal


def scrape_amazon_shoes():
    url = "https://www.amazon.com/s?k=shoes"
    
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    # Give the page some time to load
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    shoe_list = []

    for item in soup.select('.s-main-slot .s-result-item'):
        title = item.select_one('h2 .a-link-normal')
        price = item.select_one('.a-price-whole')
        image = item.select_one('.s-image')
        
        if title and price and image:
            shoe = {
                'title': title.get_text(strip=True),
                'price': price.get_text(strip=True),
                'image': image['src']
            }
            shoe_list.append(shoe)
    
    update_shoes_from_scrape(shoe_list)


    return shoe_list

def update_shoes_from_scrape(shoe_list):
    for shoe_data in shoe_list:
        shoe, created = Shoe.objects.get_or_create(
            title=shoe_data['title'],
            defaults={'image': shoe_data['image'], 'price': Decimal(shoe_data['price'])}
        )
        if not created:
            shoe.update_price(Decimal(shoe_data['price']))
            shoe.image = shoe_data['image']
            shoe.save()


# Test the scraper function independently
if __name__ == "__main__":
    shoes = scrape_amazon_shoes()
    for shoe in shoes:
        print(shoe)
