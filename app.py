from flask import Flask, request

from parser import scrape_bottle_url

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_url():
    try:
        bottle_name = scrape_bottle_url(request.form['url'])
        if bottle_name:
            return bottle_name
        else:
            return ('Unable to parse: ' + request.form['url'], 400)
    except:
        return ('Error occured in parsing', 500)
