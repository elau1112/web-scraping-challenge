from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from flask_table import Table, Col
from IPython.display import HTML


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    marsData = {}

    url1 = 'https://mars.nasa.gov/news/8915/nasas-mars-helicopter-to-make-first-flight-attempt-sunday/'
    browser.visit(url1)
    html = browser.html
    mars = BeautifulSoup(html, 'html.parser')
    results = mars.find_all('section', class_="content_page module")
    for result in results:
        marsData["news_title"] = result.find('h1', class_='article_title').text.replace('\n', '')
        marsData["news_p"] = result.find_all("p")[2].text
        marsData["news_date"] = result.find('span', class_='release_date').text.split('| ')[1].replace('\n', '')

    url12 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url12)
    xpath = './/a[@href]/button'
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    html = browser.html
    mars12 = BeautifulSoup(html, 'html.parser')
    featured = mars12.find("img", class_="fancybox-image")["src"]
    marsData["featured_img_url"] = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featured

    url14 = "https://space-facts.com/mars/"
    tables = pd.read_html(url14)
    df = tables[0]
    df1=df.rename(columns={0 :"Description", 1:"Mars"})
    marsData["html_table"] = df1.to_html(justify="left", index=False, classes='table table-striped')  

    
    url13 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response13 = requests.get(url13)
    mars13 = BeautifulSoup(response13.text, 'html.parser')

    import re
    results13 = mars13.find_all('a', {'href':re.compile('/search/map/Mars')})
    img_u=[]
    for result13 in results13:
        img_u.append('https://astrogeology.usgs.gov' + result13['href'])

    hemisphere_image=[]
    hemisphere_title=[]

    for i in range(len(img_u)):
        url_i = img_u[i]
        browser.visit(url_i)
        xpath_i = './/ul//a[@href]'
        results_i = browser.find_by_xpath(xpath_i)
        img = results_i[0]
        img.click()    
    
        response_i = requests.get(url_i)
        mars_i = BeautifulSoup(response_i.text, 'html.parser')
        results_ii=mars_i.find_all('a', {'href':re.compile('full.jpg')})

        for result_ii in results_ii:
            title=mars_i.find('h2', class_='title').text.split(' Enhanced')[0]
            img_url=result_ii['href']
            hemisphere_image.append({"img_url": img_url})
            hemisphere_title.append({"title": title})
    
    marsData["img_u"] = img_u
    marsData["h_image"] = hemisphere_image
    marsData["h_title"] = hemisphere_title

    browser.quit()
    return marsData

if __name__ == "__main__":
    data = scrape()
    print(data)