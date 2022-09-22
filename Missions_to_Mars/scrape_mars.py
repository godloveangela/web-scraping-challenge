import bs4
import lxml
import pymongo
import requests
import splinter
import selenium
import pandas as pd

def scrape():
    ans_list = []

    site = "https://redplanetscience.com/"
    featured_image_url = "https://spaceimages-mars.com/"
    mar_facts = "https://galaxyfacts-mars.com/"
    mars_hemisphere = "https://marshemispheres.com/"


    browser = splinter.Browser('chrome')
    
    # Visit the Mars News Site
    browser.visit(site)
    html = browser.html
    soup = bs4.BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_text = soup.find('div', class_='article_teaser_body').text
    print(news_title)
    print(news_text)
    ans_list.append(news_title)
    ans_list.append(news_text)

    # Visit the Mars Featured Image Site
    browser.visit(featured_image_url)
    html = browser.html
    soup = bs4.BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find('a', class_='showimg fancybox-thumbs')['href']
    featured_image_url = 'https://spaceimages-mars.com/' + featured_image_url
    print(featured_image_url)
    ans_list.append(featured_image_url)

    # Mars Facts
    table = pd.read_html(mar_facts)
    table = table[0]
    table.columns = ['Description', 'Mars', 'Earth']
    print(table)

    # table of json
    table = table.to_dict('records')
    print(table)

    # Mars Hemispheres
    emisphere_image_urls = []
    browser.visit(mars_hemisphere)
    html = browser.html
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # <a href="cerberus.html" class="itemLink product-item">
    img_tag = soup.find_all('a', class_='itemLink product-item')
    img_list = []
    for i in img_tag:
        # 取src
        # print(i['href'])
        if 'https://marshemispheres.com/' + i['href'] not in img_list and i['href'] != '#':
            img_list.append('https://marshemispheres.com/' + i['href'])
    Original_img_list = []
    for i in img_list:
        browser.visit(i)
        html = browser.html
        soup = bs4.BeautifulSoup(html, 'html.parser')
        # <a target="_blank" href="images/cerberus_enhanced.tif">Original</a>
        img_url = soup.find('a', text='Sample')
        print(img_url)
        img_dict = {}
        img_dict['title'] = soup.find('h2', class_='title').text
        img_dict['img_url'] = 'https://marshemispheres.com/' + img_url['href']
        Original_img_list.append(img_dict)

    ans_list.append(Original_img_list)
    client = pymongo.MongoClient('mongodb://admin:123456@150.158.149.214:8087/')
    db = client['mars_db']
    collection = db['mars_collection']
    collection.insert_one({'news_title': news_title, 'news_text': news_text, 'featured_image_url': featured_image_url, 'mars_facts': table, 'mars_hemisphere': Original_img_list})
    return ans_list

if __name__ == '__main__':
    scrape()
    




