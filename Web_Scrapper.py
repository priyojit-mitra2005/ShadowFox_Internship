import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the page
url = "https://books.toscrape.com"
response = requests.get(url)
response.raise_for_status() # raises error if request fails

# Step 2: Parse the HTML
soup = BeautifulSoup(response.text, "lxml")

# Step 3: Find all book titles and prices
books = soup.find_all("article", class_="product_pod")

for book in books[:5]:
    # Safely get the anchor tag and its title attribute
    h3 = book.find("h3")
    a_tag = h3.find("a") if h3 is not None else None
    title = a_tag.get("title") if a_tag is not None else "No title found"
    price_tag = book.find("p", class_="price_color")
    price = price_tag.text if price_tag is not None else "No price found"
    print(f"Title: {title} | Price: {price}")