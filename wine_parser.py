def parse_wine_data(wine_data):
	parsed_wine_data = {}
	parsed_wine_data['name'] = wine_data.find('span', class_="wine-page__header__information__details__name__vintage").text
	parsed_wine_data['image_url'] = extract_image_url(wine_data.find('div', class_="wine-page__header__information__image__wine").attrs['style'])
	parsed_wine_data['rating'] = wine_data.find('div', class_="wine-page__header__information__details__average-rating__value__number").text
	parsed_wine_data['brand'] = extract_value_and_url(wine_data.find('a', class_="wine-page__header__information__details__name__winery"))
	parsed_wine_data['brand']['type'] = 'winery'
	parsed_wine_data['reviews'] = [parse_review(review) for review in wine_data.findAll('div', class_="vintage-review-item")]
	try:
		parsed_wine_data['region'] = wine_data.find('div', text='Region', attrs={'class':"wine-page__summary__item__header"}).findNext('div', class_="wine-page__summary__item__content").text
		parsed_wine_data['style'] = wine_data.find('div', text='Regional styles', attrs={'class':"wine-page__summary__item__header"}).findNext('div', class_="wine-page__summary__item__content").text
		parsed_wine_data['grapes'] = [extract_value_and_url(grape) for grape in wine_data.findAll('a', {'data-item-type':'grape'})]
		parsed_wine_data['food_pairings'] = [extract_value_and_url(food_pairing) for food_pairing in wine_data.findAll('a', {'data-item-type':'food-pairing'})]
		parsed_wine_data['alcohol_content'] = float(wine_data.find('div', text='Alcohol', attrs={'class':"wine-page__summary__item__header"}).findNext('div', class_="wine-page__summary__item__content").text.partition('%')[0])
	except:
		pass
	parsed_wine_data['unique_name'] = parsed_wine_data['brand']['name'] + ' ' + parsed_wine_data['name']
	return parsed_wine_data

def parse_review(review_data):
	review = {}
	rating = 0
	for star in review_data.find('div', class_="vintage-review-item__rating").findAll('i'):
		if star.attrs['class'][0] == 'icon-100-pct':
			rating = rating + 1
		elif star.attrs['class'][0] == 'icon-50-pct':
			rating = rating + .5
	review['rating'] = rating
	try:
		review['note'] = review_data.find('div', class_="vintage-review-item__content__note").text
		review['date'] = review_data.find('a',text=lambda text:text and text.startswith('Rated on')).text.partition('Rated on ')[2]
	except:
		pass
	return review

def extract_image_url(tag_attr):
	return tag_attr.partition('(//')[2].partition(')')[0]

def extract_value_and_url(tag):
	return {
		'name': tag.text,
		'url': 'vivino.com' + tag.attrs['href']
	}
