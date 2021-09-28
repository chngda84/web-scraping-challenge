from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# return one Python dictionary containing all of the scraped data
mars_info = {}

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

#1 NASA Mars News

    # Visit https://redplanetscience.com/
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get news title
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    # Store data in a dictionary
    mars_info["news_title"]=news_title
    mars_info["news_p"]=news_p 

    # Close the browser after scraping
    browser.quit()

#2 Featured image

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit https://spaceimages-mars.com/
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    time.sleep(1)

    # Scrape page into Soup
    image_html = browser.html
    image_soup = bs(image_html, "html.parser")

    relative_image_path = image_soup.find("div", class_ = "header").find('div',class_="floating_text_area").a["href"]
    featured_image_url = image_url + relative_image_path

    # Store data in a dictionary
    mars_info["featured_image_url"]=featured_image_url 

    # Close the browser after scraping
    browser.quit()

#3 Facts

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    time.sleep(1)

    url = 'https://galaxyfacts-mars.com/'

    # <!-- read table -->
    tables = pd.read_html(url)
    tables

    # insert table into a df 
    df = tables[0]

    # rename headers
    cols = list(df.columns)
    cols[0] = ""
    cols[1] = "Mars"
    cols[2] = "Earth"
    df.columns = cols

    # comvert to html table
    html_table = df.to_html().replace('\n', '')

    # Store data in a dictionary
    mars_info["mars_facts"] = html_table

    # Close the browser after scraping
    browser.quit()

#4 Hemispheres

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit https://marshemispheres.com/
    hs_url = "https://marshemispheres.com/"
    browser.visit(hs_url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    hs_soup = bs(html, "html.parser")
    print(hs_soup.prettify())

    # create empty list
    hemisphere_image_urls = []

    for numbers in range(4):
    # get title
        title =  hs_soup.find_all("h3")[numbers].text

        # get html link to new page
        new_page_link = hs_soup.find_all("div", class_ = "item")[numbers].a["href"]
        new_page_url = hs_url + new_page_link
        browser.visit(new_page_url)

        # scrape info into soup
        html = browser.html
        hs_image_soup = bs(html, "html.parser")

        # get link to tif image
        tif_link = hs_image_soup.find("img",class_ = "wide-image")["src"]
        tif_url = hs_url + tif_link

        # insert into list
        hemisphere_image_urls.append({"title" : title, "img_url" : tif_url})
    
    # Store data in a dictionary
    mars_info["hemisphere_image_urls"] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info 
