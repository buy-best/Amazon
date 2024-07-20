from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from decimal import Decimal
from .models import Product, PriceHistory

KNOWN_BRANDS = [
    "New Balance", "Nike", "Adidas", "Reebok", "Puma", "Asics", "Skechers",
    "Under Armour", "Converse", "Vans", "Fila", "Brooks", "Hoka One One",
    "Merrell", "Salomon", "Timberland", "Dr. Martens", "Clarks", "Crocs",
    # Add more brands as needed
]

def extract_brand(title):
    title_words = title.split()
    for i in range(len(title_words)):
        for j in range(i+1, len(title_words)+1):
            potential_brand = " ".join(title_words[i:j])
            if potential_brand in KNOWN_BRANDS:
                return potential_brand
    return title_words[0]  # fallback to first word if no known brand is found

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
    
    # Wait for the product grid to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.s-main-slot.s-result-list')))
    
    # Scroll to load more products
    for _ in range(3):  # Adjust the range to load more or fewer products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    shoe_list = []
    
    for item in soup.select('.s-main-slot .s-result-item'):
        title_elem = item.select_one('h2 .a-link-normal')
        price_elem = item.select_one('.a-price .a-offscreen')
        image_elem = item.select_one('.s-image')
        rating_elem = item.select_one('.a-icon-star-small .a-icon-alt')
        review_count_elem = item.select_one('.a-size-base.s-underline-text')
        
        if title_elem and price_elem and image_elem:
            title = title_elem.get_text(strip=True)
            url = 'https://www.amazon.com' + title_elem['href'] if title_elem.has_attr('href') else None
            price = price_elem.get_text(strip=True)
            image = image_elem['src']
            rating = rating_elem.get_text(strip=True).split()[0] if rating_elem else 'N/A'
            review_count = review_count_elem.get_text(strip=True) if review_count_elem else 'N/A'
            
            brand = extract_brand(title)

            shoe = {
                'title': title,
                'brand': brand,
                'price': price,
                'image': image,
                'url': url,
                'rating': rating,
                'review_count': review_count
            }
            shoe_list.append(shoe)
    
    driver.quit()
    return shoe_list

def update_prices():
    shoes = scrape_amazon_shoes()
    for shoe in shoes:
        product, created = Product.objects.get_or_create(
            url=shoe['url'],
            defaults={
                'name': shoe['title'],
                'brand': shoe['brand'],
                'current_price': Decimal(shoe['price'].replace('$', '').replace(',', '')),
                'image_url': shoe['image'],
                'rating': shoe['rating'],
                'review_count': shoe['review_count']
            }
        )
        price = Decimal(shoe['price'].replace('$', '').replace(',', ''))
        if created or product.current_price != price:
            product.current_price = price
            product.brand = shoe['brand']  # Update brand in case it was extracted incorrectly before
            product.rating = shoe['rating']
            product.review_count = shoe['review_count']
            product.save()
            PriceHistory.objects.create(product=product, price=price)
            auto_buys = product.auto_buys.filter(target_price__gte=price, bought=False)
            for auto_buy in auto_buys:
                user = auto_buy.user
                if user.balance >= price:
                    user.balance -= price
                    user.save()
                    auto_buy.bought = True
                    auto_buy.save()

# Test the scraper function independently
if __name__ == "__main__":
    shoes = scrape_amazon_shoes()
    for shoe in shoes:
        print(shoe)