

import bs4
import lxml
import pymongo
import requests
import splinter
import selenium
from flask import Flask, render_template
from scrape_mars import scrape


app = Flask(__name__)


@app.route('/')
def hello_world():
    client = pymongo.MongoClient('mongodb://admin:123456@150.158.149.214:8087/')
    db = client['mars_db']
    collection = db['mars_collection']
    
    data = collection.find().sort('_id', -1).limit(1)
    i = data[0]
    print(i['mars_hemisphere'])
    

    return render_template('index.html', news_title=i['news_title'], news_text=i['news_text'], featured_image_url=i['featured_image_url'], mars_facts=i['mars_facts'], mars_hemisphere=i['mars_hemisphere'])


@app.route('/scrape')
def scrapeee():
    return scrape()


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=9000, debug=True)
