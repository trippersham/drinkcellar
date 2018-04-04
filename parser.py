# coding=utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
import os.path
from base64 import b64encode
import json
from datetime import datetime
from urllib.parse import urlparse
from wine_parser import parse_wine_data
from beer_parser import parse_beer_data
from google_datastore_manager import create_entity

def hash_url(url):
	return str(b64encode(url.encode())) + '.html'

def load_rendered_site_from_cache(url):
	filename = hash_url(url)
	if os.path.isfile('rendered_page_cache/' + filename):
		with open('rendered_page_cache/' + filename, 'r') as file:
			return file.read().replace('\n', '')

def write_rendered_site_to_cache(url, source):
	filename = hash_url(url)
	with open('rendered_page_cache/' + filename, 'w') as file:
		file.write(source)

def get_parsed_rendered_site(url):
	site = load_rendered_site_from_cache(url)
	if site:
		return BeautifulSoup(site, 'html.parser')
	else:
		driver = webdriver.Chrome('./chromedriver')
		driver.get(url)
		write_rendered_site_to_cache(url, driver.page_source)
		return BeautifulSoup(driver.page_source, 'html.parser')

def scrape_bottle_url(url):
	domain = urlparse(url).netloc
	bottle_data = {}
	if domain == 'www.vivino.com':
		bottle_data = parse_wine_data(get_parsed_rendered_site(url))
		bottle_data['type'] = 'wine'
		# with open('wines/' + wine_name + '.json', 'w') as file:
		# 	json.dump(wine_data, file)
	elif domain == 'untappd.com':
		bottle_data = parse_beer_data(get_parsed_rendered_site(url))
		bottle_data['type'] = 'beer'
		# with open('beers/' + beer_name + '.json', 'w') as file:
		# 	json.dump(beer_data, file)
	else:
		raise ValueError(domain + ' is not currently supported')
	create_entity('BottleData', bottle_data, unique_name=bottle_data['unique_name'])
	return bottle_data

print(scrape_bottle_url('https://www.vivino.com/wineries/dutton-goldfield-winery/wines/riesling-chileno-valley-vineyard-9999?ref=navigation-search'))
