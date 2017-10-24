import requests
from bs4 import BeautifulSoup, Tag
import re
from . import db
from .models import AuctionSite, Listing

def scrape_all():
	add_site_to_db_if_new('TK Wine')
	scrape_tkwine()
	add_site_to_db_if_new('Spectrum')
	scrape_spectrum()
	add_site_to_db_if_new('Winebid')
	scrape_winebid()

def scrape_tkwine():
	"""
	Scrapes TKWine ebay auction site for current listings prices
	"""
	def get_years(bottles):
		years = []
		for bottle in bottles:
			year = None
			bottle_info = bottle.get_text().strip()
			if re.match(r'([1-2][0-9][0-9][0-9]).*', bottle_info):
				year = re.sub(r'([1-2][0-9][0-9][0-9])(.*)', r'\1', bottle_info)

			years.append(year)
		return years

	def get_producers(bottles):
		producers = []
		for bottle in bottles:
			bottle_info = bottle.get_text().strip()
			if re.match(r'([1-2][0-9][0-9][0-9]).*', bottle_info):
				producer = re.sub(r'([1-2][0-9][0-9][0-9])(.*)', r'\2', bottle_info)
			else:
				producer = bottle_info
			
			producers.append(producer)
		return producers


	page = requests.get("http://stores.ebay.com/tkwine")

	soup = BeautifulSoup(page.content, 'lxml')
	bottles = soup.find_all('div', class_='title')
	bottles.extend(soup.find_all('div', class_='desc'))

	# Separate year from producer
	years = get_years(bottles)
	producers = get_producers(bottles)

	# Find prices for all bottles
	prices = soup.find_all('div', class_='price')

	for item in soup.find('div', class_='curr'):
		if item.parent.class_ == 'price_bin':
			prices.append(item)

	#for year, producer, price in zip(years, producers, prices):
	#	print(year, producer, price.get_text())


def scrape_spectrum():
	"""
	Scrapes Spectrum Wine Auctions
	"""
	def scrape_page(pageUrl):
		page = requests.get('http://spectrumwineretail.com' + pageUrl)
		soup = BeautifulSoup(page.content, 'lxml')
		items = soup.select('div.product-list-options h5 a')
		prices = soup.select('span.product-list-cost-value')

		# Remove all newline values from items
		#items = [item for item in items if isinstance(item, Tag)]
		#print(items)
		for item, price in zip(items, prices):
			producer = re.sub(r'(.+)([0-9][0-9][0-9][0-9]).*', r'\1', item.text)
			year = re.sub(r'(.+)([0-9][0-9][0-9][0-9]).*', r'\2', item.text)
			print(producer, year, price.text)

		link = soup.find('a', class_='pager-item-next')
		if link != None:
			scrape_page(link['href'])



	home_page = requests.get('http://spectrumwineretail.com/country.aspx')
	soup = BeautifulSoup(home_page.content, 'lxml')
	#soup.find_all('div', class_='category-list-item-head')
	links = soup.select('div.category-list-item-head a')
	#for link in links:
	#	scrape_page(link['href'])

def scrape_winebid():
	"""
	Scrapes WineBid for current listings prices
	"""
	def scrape_page(pageUrl):
		# Scrapes single page for wine listing info
		page = requests.get('https://www.winebid.com' + pageUrl)
		soup = BeautifulSoup(page.content, 'lxml')
		
		items = soup.find('div', class_='itemResults').contents
		
		# Remove all strings from items list
		items = [item for item in items if isinstance(item, Tag)]

		for item in items:
			
			item_info = item.find('div', class_='info')
			name = item_info.find('p', class_='name').find('a').text
			try:
				itemAlerts = item_info.find('div', class_='itemAlerts').find('p').text
			except:
				itemAlerts = 'None'
			price = item.find('div', class_='price').find('a').text
			
			#print(name, itemAlerts, price)

		# Find link to next page and make a recursive call
		link = soup.find('span', class_='pageNavigation').contents[-2]
		if 'NEXT' in link.descendants:
			scrape_page(link['href'])

	home_page = requests.get("https://www.winebid.com/BuyWine")
	soup = BeautifulSoup(home_page.content, 'lxml')

	# Navigate to 'Buy Now' page
	link = soup.find('a', text='Shop Buy Now')
	
	# Make recursive call to scrap the Buy Now section of the site
	scrape_page(link['href'])
	

def add_site_to_db_if_new(site_name):
	if db.session.query(AuctionSite.id).filter( \
			AuctionSite.name==site_name).scalar() is None:
		new_site = AuctionSite(name=site_name)
		db.session.add(new_site)
		db.session.commit()




if __name__ == "__main__":
	scrape_tkwine()
	
