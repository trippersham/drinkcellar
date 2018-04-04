import text_utils

def parse_beer_data(beer_data):
    parsed_beer_data = {}
    parsed_beer_data['name'] = beer_data.find('div', class_='name').findNext('h1').text
    parsed_beer_data['image_url'] = beer_data.find('div', class_='photo-boxes').findNext('img').attrs['data-original']
    parsed_beer_data['rating'] = beer_data.find('span', class_='num').text.partition("(")[2].partition(")")[0]
    parsed_beer_data['brand'] = {
        'name': beer_data.find('p', class_='brewery').findNext('a').text,
        'type': 'brewery'
    }
    parsed_beer_data['style'] = beer_data.find('p', class_='style').text
    parsed_beer_data['description'] = beer_data.find('div', class_='beer-descrption-read-less').text.partition('Show Less')[0]
    parsed_beer_data['alcohol_content'] = float(beer_data.find('p', class_='abv').text.partition('% ABV')[0])
    parsed_beer_data['reviews'] = [parse_review(review) for review in beer_data.find('div', id='main-stream').findAll('div', class_='item')]
    parsed_beer_data['unique_name'] = parsed_beer_data['brand']['name'] + ' ' + parsed_beer_data['name']
    return parsed_beer_data

def parse_review(review_data):
    review = {}
    review['date'] = review_data.find('a', class_='timezoner').attrs['data-gregtime']
    try:
        review['rating'] = float(review_data.find('div', class_='rating-serving').find('span').attrs['class'][2].partition('r')[2])/100
    except:
        pass
    try:
        review['note'] = review_data.find('p', class_='comment-text').text
    except:
        pass
    return review
