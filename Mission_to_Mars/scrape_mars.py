from bs4 import BeautifulSoup as bs
from splinter import Browser
import urllib
import pandas as pd
import re
import time


def init_browser():
    executable_path = {"executable_path": "/Windows/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Connect to NASA News and scrape 1st article title and description
    url = 'https://mars.nasa.gov/news/'


    browser.visit(url)
    time.sleep(3)
    html_code = browser.html
    soup = bs(html_code, 'html.parser')



    news_title = soup.find_all('div', class_ = 'content_title')[1].text
    news_title = news_title.strip('\n')

    mars_data.update({'news_title': news_title})

    news_p = soup.find('div', class_ = 'article_teaser_body').text


    mars_data.update({'news_p': news_p})

    # Scrape website for featured image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(image_url)
    image_html = browser.html
    soup_i = bs(image_html, 'html.parser')


    featured_image = soup_i.find('a', class_= 'button fancybox').get('data-fancybox-href')


    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image
    featured_image_url
    mars_data.update({'featured_image_url': featured_image_url})

    # Scrape twitter account for most recent weather tweet info
    weather_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(weather_url)
    time.sleep(3)
    tweet_html = browser.html
    soup_w = bs(tweet_html, 'html.parser')


    mars_weather_i = soup_w.find('span', text=re.compile('InSight')).text
    mars_weather = mars_weather_i.replace('\n', ' ')
    mars_weather
    mars_data.update({'mars_weather': mars_weather})

    # Scrape site for table about Mars facts
    facts_url = 'https://space-facts.com/mars/'

    browser.visit(facts_url)
    facts_html = browser.html
    soup_f = bs(facts_html, 'html.parser')


    mars_facts = pd.read_html(facts_url)[0]
    mars_facts = mars_facts.rename(columns= {0: 'Description', 1: 'Value'})


    mars_facts.set_index('Description', inplace = True)


    html_table = mars_facts.to_html()

    mars_data.update({'mars_info_table': html_table})

    # Scrape site for names of hemispheres and links to images
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemis_url)
    time.sleep(3)
    hemis_html = browser.html
    soup_h = bs(hemis_html, 'html.parser')


    names_list = []

    hemis_name = soup_h.find_all('a', class_= 'itemLink product-item')


    for item in hemis_name:
        try:
            name = item.find('h3').text.strip('Enhanced')
            names_list.append(name)
        except:
            print('name not avaliable')



    hemisphere_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
    url_list = []
    for link in hemisphere_urls:
        browser.visit(link)
        time.sleep(3)
        hemis_ind_html = browser.html
        soup_hi = bs(hemis_ind_html, 'html.parser')
        hemis_ind_url = soup_hi.find('li').find('a').get('href')
        url_list.append(hemis_ind_url)

        

    hemisphere_image_urls = [{'title': names_list[0], 'img_url': url_list[0]},
                            {'title': names_list[1], 'img_url': url_list[1]},
                            {'title': names_list[2], 'img_url': url_list[2]},
                            {'title': names_list[3], 'img_url': url_list[3]}]


    mars_data.update({'hemisphere_image_urls': hemisphere_image_urls})

    return(mars_data)