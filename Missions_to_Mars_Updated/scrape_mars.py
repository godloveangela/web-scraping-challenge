import bs4
import splinter
import pandas as pd


def scrape():
    site = "https://redplanetscience.com/"
    featured_image_url = "https://spaceimages-mars.com/"
    mar_facts = "https://galaxyfacts-mars.com/"
    mars_hemisphere = "https://marshemispheres.com/"

    with splinter.Browser('chrome') as browser:
        # Visit the Mars News Site
        browser.visit(site)
        html = browser.html
        soup = bs4.BeautifulSoup(html, 'html.parser')
        news_title = soup.find('div', class_='content_title').text
        news_text = soup.find('div', class_='article_teaser_body').text
        print(news_title)
        print(news_text)

        # Visit the Mars Featured Image Site
        browser.visit(featured_image_url)
        html = browser.html
        soup = bs4.BeautifulSoup(html, 'html.parser')
        featured_image_url = soup.find(
            'a', class_='showimg fancybox-thumbs')['href']
        featured_image_url = 'https://spaceimages-mars.com/' + featured_image_url
        print(featured_image_url)

        # Mars Facts
        table = pd.read_html(mar_facts)
        table = table[0]
        table.columns = ['Description', 'Mars', 'Earth']
        print(table)

        # table of json
        table = table.to_dict('records')
        print(table)

        # Mars Hemispheres
        browser.visit(mars_hemisphere)
        html = browser.html
        soup = bs4.BeautifulSoup(html, 'html.parser')
        # <a href="cerberus.html" class="itemLink product-item">
        img_tag = soup.find_all('a', class_='itemLink product-item')
        img_list = []
        for i in img_tag:
            # print(i['href'])
            if 'https://marshemispheres.com/' + i['href'] not in img_list and i['href'] != '#':
                img_list.append('https://marshemispheres.com/' + i['href'])
        lst_hemisphere_images = []
        for i in img_list:
            browser.visit(i)
            html = browser.html
            soup = bs4.BeautifulSoup(html, 'html.parser')
            # <a target="_blank" href="images/cerberus_enhanced.tif">Original</a>
            img_url = soup.find('a', text='Sample')
            print(img_url)
            img_dict = {}
            img_dict['title'] = soup.find('h2', class_='title').text
            img_dict['img_url'] = 'https://marshemispheres.com/' + \
                img_url['href']
            lst_hemisphere_images.append(img_dict)

    res = {'news_title': news_title, 'news_text': news_text, 'featured_image_url':
           featured_image_url, 'mars_facts': table, 'hemisphere_image_urls': lst_hemisphere_images}

    return res


if __name__ == '__main__':
    scrape()
