import requests
from bs4 import BeautifulSoup, Tag
import re

count = 0

def scrape_tkwine():
	"""
	Scrapes TKWine ebay auction site for current listings prices
	"""

	page = requests.get("http://stores.ebay.com/tkwine")

	soup = BeautifulSoup(page.content, 'lxml')
	titles = soup.find_all('div', class_='title')
	titles.extend(soup.find_all('div', class_='desc'))

	prices = soup.find_all('div', class_='price')

	for item in soup.find('div', class_='curr'):
		if item.parent.class_ == 'price_bin':
			prices.append(item)

	for title, price in zip(titles, prices):
		print(title.get_text().strip(), price.get_text())



def scrape_winebid():
	"""
	Scrapes WineBid for current listings prices
	"""

	def scrape_page(pageUrl):
		global count
		count += 1
		# Scrapes single page for wine listing info
		page = requests.get('https://www.winebid.com' + pageUrl)
		soup = BeautifulSoup(page.content, 'lxml')
		
		items = soup.find('div', class_='itemResults').contents
		for item in items:
			if isinstance(item, Tag):
				item_info = item.find('div', class_='info')
				name = item_info.find('p', class_='name').find('a').text
				try:
					itemAlerts = item_info.find('div', class_='itemAlerts').find('p').text
				except:
					itemAlerts = 'None'
				price = item.find('div', class_='price').find('a').text
				print(name, itemAlerts, price)

		# Find next link and scrape next page (recursive call)
		link = soup.find('span', class_='pageNavigation').contents[-2]
		if 'NEXT' in link.descendants:
			scrape_page(link['href'])
			
	home_page = requests.get("https://www.winebid.com/BuyWine")
	soup = BeautifulSoup(home_page.content, 'lxml')

	# Navigate to 'Buy Now' page
	link = soup.find('a', text='Shop Buy Now')
	
	# Make recursive call to scrap the Buy Now section of the site
	scrape_page(link['href'])


		



	


if __name__ == "__main__":
	scrape_winebid()
	print(count)
