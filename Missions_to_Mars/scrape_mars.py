###################################################
# Mission to Mars - Scraping
###################################################

#import dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

#create the scrape function
def scrape():
    ###################################################
    # News Scraping
    ###################################################

    #define url to scrape for news
    news_url = 'https://mars.nasa.gov/news/'

    #get the page
    news_response = requests.get(news_url)
    #make beautifulsoup object
    news_soup = BeautifulSoup(news_response.text, 'lxml')

    #find the first title and paragraph text (classes pulled from inspecting the url)
    news_title = news_soup.find(class_='content_title').text
    news_p = news_soup.find(class_='rollover_description_inner').text

    ###################################################
    # Featured Mars Image
    ###################################################

    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #define url to scrape for images
    mars_img_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    #run the mars image site
    browser.visit(mars_img_url)

    #browse through mars images site
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #pull the the featured image (class pulled from inspecting the url)
    featured_image = img_soup.find('a', class_='showimg fancybox-thumbs')
    featured_image_link = featured_image['href']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featured_image_link

    #close browser
    browser.quit()

    ###################################################
    # Mars Facts
    ###################################################

    #mars facts url
    facts_url = 'https://space-facts.com/mars/'

    #read the content from the facts_url
    fact_table = pd.read_html(facts_url)

    #pull just the first table of mars facts
    facts_df = fact_table[0]

    #rename the columns and re-index the df
    facts_df.rename(columns={0: 'Fact', 1: 'Description'}, inplace=True)
    facts_df.set_index('Fact', inplace=True)

    #convert df to an html table
    facts_html_table = facts_df.to_html()

    #remove unnecessary new lines
    formatted_facts_html_table = facts_html_table.replace('\n', '')

    ###################################################
    # Mars Hemispheres
    ###################################################

    #define urls to scrape for images
    cerberus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    schiaparelli_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    syrtis_major_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    valles_marineris_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    #hold all urls in one list to iterate through
    hemisphere_urls = [cerberus_url, schiaparelli_url, syrtis_major_url, valles_marineris_url]

    #list to hold image urls
    hemi_img_urls = []

    #iterate through url list
    for hemisphere in hemisphere_urls:
        #get the page
        response = requests.get(hemisphere)
        #make beautifulsoup object
        soup = BeautifulSoup(response.text, 'lxml')
        #find the url (divs and classes found by inspecting the urls)
        #variables named for the level of html they are on
        div = soup.find('div', class_='downloads')
        ul = div.find('ul')
        li = ul.find('li')
        a = li.find('a')
        href = a['href']
        #append href to hemi_img_urls list
        hemi_img_urls.append(href)

    #save hemisphere titles to list
    hemisphere_titles = ['Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere', 'Valles Marineris Hemisphere']

    #put titles to their mathcing urls in dictionaries
    hemi_img_url_dicts = [
        {'title': hemisphere_titles[0], 'img_url': hemi_img_urls[0]},
        {'title': hemisphere_titles[1], 'img_url': hemi_img_urls[1]},
        {'title': hemisphere_titles[2], 'img_url': hemi_img_urls[2]},
        {'title': hemisphere_titles[3], 'img_url': hemi_img_urls[3]},
    ]

    ###################################################
    #return scraped data in a dictionary
    mars_info = {
                'Mars_News_Title': news_title,
                'Mars_News_Text': news_p,
                'Featured_Image': featured_image_url,
                'Mars_Facts': formatted_facts_html_table,
                'Mars_Hemisphere_1': hemi_img_url_dicts[0],
                'Mars_Hemisphere_2': hemi_img_url_dicts[1],
                'Mars_Hemisphere_3': hemi_img_url_dicts[2],
                'Mars_Hemisphere_4': hemi_img_url_dicts[3]
                }

    return mars_info

###################################################
