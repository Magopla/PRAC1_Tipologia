import time
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

UserAgent =  ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

URL = "https://www.amazon.es/alm/storefront/ref=grocery_amazonfresh?almBrandId=QW1hem9uIEZyZXNo"
BASEURL = "https://www.amazon.es"

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(URL)
time.sleep(1)
html = browser.page_source

soup = BeautifulSoup(html, "lxml")

navigatorBar = soup.find(attrs={'id':'nav-subnav'})

subPages = navigatorBar.findAll(attrs={'class':'nav-a'})



subApartats = {}
headerNavBar = soup.find("header", attrs={"id":"navbar-main"})
div = headerNavBar.find("div", attrs = {"id":"navbar"})



for subPage in subPages:
    if subPage.find(attrs={'class':"nav-arrow"}) and not subPage.find('img'):

        divMenu = soup.find('div', attrs={"id":"nav-flyout-"+subPage['data-nav-key']})

        subSubPages = divMenu.findAll('a',attrs={"class":"generic-subnav-flyout-link"})

        SSpages = {}

        for subSubPage in subSubPages:
            nom = subSubPage.find('div', attrs={'class':'generic-subnav-flyout-title'})
            if nom:
                SSpages[nom.get_text().strip()] = subSubPage['href']
        subApartats[subPage['aria-label']] = {
            'href': subPage['href'],
            'data-nav-key': subPage['data-nav-key'],
            'pages':SSpages
        }

for apartat in subApartats:
    print("************************")
    print(subApartats[apartat])
    print("************************")

    for page in subApartats[apartat]['pages']:
        print(page)
        try:
            url = BASEURL+subApartats[apartat]['pages'][page]
            browser.get(url)
            time.sleep(1)
            html = browser.page_source
            soupSubPage = BeautifulSoup(html, "lxml")
            categories = soupSubPage.findAll('h2', attrs={'class':'a-size-large'})


            for categoria in categories:

                nomCategoria  = categoria.find('span').get_text()
                urlCategoria =BASEURL + categoria.find('a')['href']
                print(nomCategoria)
                browser.get(urlCategoria)
                time.sleep(1)
                html = browser.page_source
                soupCategoria = BeautifulSoup(html, "lxml")
                print("--------------------------------")
                seccioDivs = soupCategoria.find('div', attrs={'class':'s-main-slot s-result-list s-search-results sg-row'})
                divs = seccioDivs.findAll('div')
                for div in divs:
                    if div.has_attr('data-asin') and div['data-asin']!="":
                        titol = div.find("h2").get_text()
                        priceWhole = div.find("span", attrs={"class":"a-price-whole"}).get_text()
                        priceSymbol = div.find("span", attrs={"class":"a-price-symbol"}).get_text()
                        priceUnity = div.find("span", attrs={"class":"a-size-base a-color-secondary"}).get_text()
                        print(apartat,page,nomCategoria, titol,priceWhole, priceSymbol, priceUnity)


        except WebDriverException:
            print("error")

