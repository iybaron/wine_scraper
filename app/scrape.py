import os
import sys
import re
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup, Tag
from . import db
from .models import AuctionSite, Listing


def scrape_all():
	scrape_tkwine()
	scrape_spectrum()
	scrape_winebid()


def scrape_tkwine():
	"""
	Scrapes TKWine ebay auction site for current listings prices
	"""
	site_name = 'TK Wine'
	add_site_to_db_if_new(site_name)
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
			
			producers.append(producer.strip())
		return producers

	def get_item_codes(bottles):
		item_codes = []
		for bottle in bottles:
			link = bottle.find('a')['href']
			item_code = re.sub(r'(.*)(/)([0-9]+)', r'\3', link)
			item_codes.append(item_code)
		return item_codes

	page = requests.get("http://stores.ebay.com/tkwine")

	soup = BeautifulSoup(page.content, 'lxml')
	bottles = soup.find_all('div', class_='title')
	bottles.extend(soup.find_all('div', class_='desc'))

	# Separate needed information html tag objects
	years = get_years(bottles)
	producers = get_producers(bottles)
	item_codes = get_item_codes(bottles)

	# Find prices for all bottles
	price_tags = soup.find_all('div', class_='price')
	price_tags.extend(soup.select('.price_bin div.curr'))

	prices = []
	for tag in price_tags:
		price = re.sub(r'(.*)(\$)([0-9]+\.[0-9][0-9])(.*)', r'\2\3', tag.get_text())
		prices.append(price)

	for year, producer, price, item_code in zip(years, producers, prices, item_codes):
		add_row_to_db_if_new(year, producer, price, item_code, site_name)


def scrape_spectrum():
	"""
	Scrapes Spectrum Wine Auctions
	"""
	site_name = 'Spectrum'
	add_site_to_db_if_new(site_name)

	def get_item_codes(soup):
		item_codes = []
		input_objects = soup.select('div.product-list-control input')
		for input_object in input_objects:
			attribute_with_code = input_object['onclick']
			item_code = re.sub(r'(.*)(productList)([0-9]+)(.*)', r'\3', attribute_with_code)
			item_codes.append(item_code)
		return item_codes

	def scrape_page(pageUrl):
		page = requests.get('http://spectrumwineretail.com' + pageUrl)
		soup = BeautifulSoup(page.content, 'lxml')
		
		items = soup.select('div.product-list-options h5 a')
		prices = soup.select('span.product-list-cost-value')
		item_codes = get_item_codes(soup)
		
		for item, price, item_code in zip(items, prices, item_codes):
			if re.match(r'(.+)([0-9][0-9][0-9][0-9]).*', item.text):
				producer = re.sub(r'(.+)([0-9][0-9][0-9][0-9]).*', r'\1', item.text)
				year = re.sub(r'(.+)([0-9][0-9][0-9][0-9]).*', r'\2', item.text)
			else:
				producer = item.text
				year = None
			add_row_to_db_if_new(year, producer, price.text, item_code, site_name)

		link = soup.find('a', class_='pager-item-next')
		if link != None:
			scrape_page(link['href'])



	home_page = requests.get('http://spectrumwineretail.com/country.aspx')
	soup = BeautifulSoup(home_page.content, 'lxml')
	links = soup.select('div.category-list-item-head a')
	for link in links:
		scrape_page(link['href'])


def scrape_winebid():
	"""
	Scrapes WineBid for current listings prices
	"""
	site_name = 'Winebid'
	add_site_to_db_if_new(site_name)
	def scrape_page(pageUrl):
		# Scrapes single page for wine listing info
		page = requests.get('https://www.winebid.com' + pageUrl)
		soup = BeautifulSoup(page.content, 'lxml')
		
		items = soup.find('div', class_='itemResults').contents
		
		# Remove all strings from items list
		items = [item for item in items if isinstance(item, Tag)]

		for item in items:
			
			info_tag = item.find('div', class_='info')
			listing_text = info_tag.find('p', class_='name').find('a').text
			
			if re.match(r'([1-2][0-9][0-9][0-9])(.*)', listing_text):
				year = re.sub(r'([1-2][0-9][0-9][0-9])(.*)', r'\1', listing_text)
				producer = re.sub(r'([1-2][0-9][0-9][0-9])(.*)', r'\2', listing_text)
			else:
				year = None
				producer = listing_text

			try:
				item_alerts = info_tag.find('div', class_='itemAlerts').find('p').text.strip()
			except:
				item_alerts = None

			price = item.find('div', class_='price').find('a').text
			item_code = item['data-item-id']

			add_row_to_db_if_new(year, producer, price, item_code, \
								site_name, item_alerts)

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
	session = get_active_db_session()

	if session.query(AuctionSite.id).filter( \
			AuctionSite.name==site_name).scalar() is None:
		new_site = AuctionSite(name=site_name)
		session.add(new_site)
		session.commit()


def add_row_to_db_if_new(year, producer, price, item_code, site, alert=None):
	session = get_active_db_session()

	if session.query(Listing.id).filter( \
			Listing.item_code==item_code).scalar() is None:
		site_id = session.query(AuctionSite.id).filter(AuctionSite.name==site)

		if site_id is not None:
			new_listing = Listing(year=year, producer=producer, alert=alert, \
							price=price, item_code=item_code, site_id=site_id)
			session.add(new_listing)
			session.commit()


def create_db_session():
	"""
	Connect to database when scrape_all is called outside of full app
	"""
	engine = create_engine(
			'mysql+mysqlconnector://root:' + os.getenv('DB_PASS') + \
			'@localhost:3306/wine_scraper_devdb'
	)

	Session = sessionmaker(bind=engine)
	session = Session()

	return session


def get_active_db_session():
	"""
	Return db.session if app is running, or create a new session if not
	"""
	if(os.getenv('CRON_JOB') == '1'):
		session = create_db_session()
	else:
		session = db.session

	return session


if __name__ == "__main__":
	scrape_all()
	
