from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd
import sys
from pprint import pprint

#define  function on path for chromedriver.exe.  
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {'executable_path': 'C:/ChromeSafe/chromedriver.exe'}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    Mars_dict=dict()
    heremisphere_image_urls=[]
    

    # Visit url of page to be scrapped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    #Scrap page into soup. 
    soup = bs(html, 'html.parser')

    firstslide = soup.select_one('ul.item_list li.slide')
    secondtitle = firstslide.find("div", class_='content_title').get_text()
    
    firstparagraph = firstslide.find("div", class_='article_teaser_body').get_text()
    Mars_dict["News_title"]=secondtitle
    Mars_dict["News_p"]=firstparagraph


    # Visit mars space images - featured image
    url1 ='https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA17838'
    browser.visit(url1)
    html1 = browser.html
    soup1 = bs(html1, 'html.parser')

    time.sleep(1)


    image_url = soup1.select_one('figure.lede a img').get("src")
    # image_url
    featured_image_url = "https://www.jpl.nasa.gov"+ image_url
    # featured_image_url
    #add to dictionary
    Mars_dict["feature_image_url"]=featured_image_url

    #browser.quit()

    # Mars Weather tweet
    url2 = 'https://twitter.com/marswxreport?lang=en'
    
    # browser = init_browser()
    # html2 = browser.html
    # soup2 = bs(html2, 'html.parser')
    #browser = init_browser()
    browser.visit(url2)

    
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')

    timeline_url = soup2.select_one('div.content div.js-tweet-text-container')
    mars_weather = timeline_url.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    print(mars_weather, file=sys.stdout)

# #     timeline_url = soup2.select_one('div.content div.js-tweet-text-container')
#    
# #     mars_weather = timeline_url.find('p').text
#     # add to dictionary
    Mars_dict["Mars_tweet"]=mars_weather


    # Mars Facts
    url3 = 'http://space-facts.com/mars/'
   

    Marsfact_df = pd.read_html(url3)
    mf_df = Marsfact_df[0]
    mf_df.head()

    # rename columns
    marsf_df = mf_df.rename(columns={0: "Facts", 1:"Values"})
    marsf_df.head()

    # convert to html/ create html and save to file that can be opened in the browser
    marsf_df.to_html("marsfacts.html")

    # another version for passing into a variable to print
    html9 = marsf_df.to_html()
    

    Mars_dict["Marsfacts.html"] = html9


    # Mars Hemisphere
    print("starting hemisphere scrape")
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)

    html5 = browser.html
    soup5 = bs(html5, "html.parser")

    time.sleep(10)

    data = soup5.find('div', class_="collapsible results")
    #four_data = data.find_all('div',class_='item')
    four_data = data.find_all('div', class_="description")
    pprint('going into loop')
    count = 0
    for tag in four_data:
        pprint(tag)
        count += 1
        print(str(count))
        title = tag.find('h3').text
        pprint(title)
        #title_l.append(title)
        
        #while looping through, create a link for each with access to the full image url
        link  = "https://astrogeology.usgs.gov" + tag.find('a',class_='itemLink product-item')['href']
        #print(link)
    
        #browse each link 
        browser.visit(link)
        time.sleep(10)
    
        html6   = browser.html
        soup6 = bs(html6, 'html.parser')
        four_image = soup6.find('div', class_='downloads')
        four_images=four_image.li.a['href']
        pprint(four_images)
    
        # create a dictionary for each loop
        Mars_hmsph = dict()  
        #add to the dictionary at each loop
        Mars_hmsph['title']= title
        Mars_hmsph['img_url']= four_images
        
    
        # to get all four append in list
        heremisphere_image_urls.append(Mars_hmsph)
        print('printing hermishper image urls')
        pprint(heremisphere_image_urls)
    Mars_dict["Heremisphere"] = heremisphere_image_urls
    print('mars dictionary')
    pprint(Mars_dict)

        # Dictionary to be inserted as a MongoDB document
    post = {
            'Title': Mars_dict["News_title"],
            'News': Mars_dict["News_p"],
            'Featured Image': Mars_dict["feature_image_url"],
            'Weather Tweet' : Mars_dict["Mars_tweet"],
            'Mars Facts' : Mars_dict["Marsfacts.html"],
            'Hsphere' : Mars_dict["Heremisphere"],   
            }
    print('printing post')
    pprint(post)
        
        
    return post

mars_result=scrape()
pprint(mars_result)