import requests
from bs4 import BeautifulSoup

"""
Scrapes TKWine ebay action site for current listings
prices
"""

page = requests.get("http://stores.ebay.com/tkwine")

soup = BeautifulSoup(page.content, 'html.parser')
titles = soup.find_all('div', class_='title')
titles.extend(soup.find_all('div', class_='desc'))

prices = soup.find_all('div', class_='price')

for item in soup.find_all('div', class_='curr'):
	if item.parent.class_ == 'price bin':
		prices.append(item)

for title, price in zip(titles, prices):
	print title.get_text().strip(), price.get_text()




