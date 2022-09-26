import pymongo
from flask import Flask, render_template, redirect
from scrape_mars import scrape


app = Flask(__name__)
mongo_uri = 'mongodb://admin:123456@150.158.149.214:8087/'


@app.route('/')
def hello_world():
    client = pymongo.MongoClient(mongo_uri)
    db = client['mars_db']
    collection = db['mars_collection']

    data = collection.find_one()
    print(data)
    return render_template('index.html', mars=data)


@app.route('/scrape')
def scrapeee():
    res = scrape()
    client = pymongo.MongoClient(mongo_uri)
    db = client['mars_db']
    collection = db['mars_collection']
    if res:
        collection.drop()
        collection.insert_one(res)

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
