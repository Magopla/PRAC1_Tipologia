import time
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date
import requests
import pandas as pd
import json
import shutil
import re





class UlaboxScrapper:

    def __init__(self):
        self.url = "https://www.ulabox.com/ca/categoria/alimentacio/895?ula_src=&ula_mdm=header_bar&ula_cmp=main_category"
        self.baseUrl = "https://www.ulabox.com"
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def __get_soup(self, url):
        """
        Donat un enllaç obtenim el fitxer en format soup.
        """
        print(url)
        soup = self.__get_soup_from_url(url)
        while soup is None:
            print("Error obtenin el soup de la pagina web, reintentant")
            time.sleep(1)
            soup = self.__get_soup_from_url(url)
        return soup

    def __get_soup_from_url(self, url):
        """
        Obtenim soup donada una url
        """
        try:
            self.browser.get(url)
            time.sleep(1)
            html = self.browser.page_source
        except WebDriverException as e:
            print("Error obtenin el fitxer: ",e.msg)
            return None
        soup = BeautifulSoup(html, "lxml")
        return soup

    def __get_all_categories_urls(self, url):
        """
        Donada una pagina web, obte totes les categories.
        """
        soup = self.__get_soup(url)
        menuCategories = soup.find('ul', attrs={'class': "MuiList-root MuiList-dense MuiList-padding"})
        categories = {}
        for categoria in menuCategories.findAll('li'):
            elemA = categoria.find('a')
            url = elemA['href']
            text = elemA.get_text().strip()
            categories[text] = url
        return categories

    def __get_all_subcategories_urls(self):
        """
        Retorna totes les categories i subcategories i els seus enllaços
        """
        categories = self.__get_all_categories_urls(self.url)
        for categoria in categories:
            print("categoria")
            print(categories[categoria])
            categories[categoria] = self.__get_all_categories_urls(self.baseUrl + categories[categoria])
        return categories

    def __get_subcategory_products(self, url):
        """
        Donat un enllaç d'una subcategoria, retorna els enllaços de tots els productes llistats en aquesta pagina web
        """
        print("Subcategoria")
        soup = self.__get_soup(url)

        productes = set()
        elemsA = soup.findAll('a')
        for elem in elemsA:
            if elem.has_attr('href'):
                enllac = elem['href']
                if 'producte' in enllac:
                    productes.add(enllac)

        nextPage = soup.find('a', attrs={"rel": 'next'})
        if len(productes) == 60 and nextPage:
            productes = productes.union(self.__get_subcategory_products(self.baseUrl + nextPage['href']))
        return productes

    def get_products(self):
        """
        Obtenir un diccionari amb tots els enllaços dels productes i les seves categories i subcategories
        """
        urls = self.__get_all_subcategories_urls()
        for categoria in urls:
            for subcategoria in urls[categoria]:
                urls[categoria][subcategoria] = self.__get_subcategory_products(
                    self.baseUrl + urls[categoria][subcategoria])


        return urls

    def __del__(self):
        self.browser.close()

    def scraper_web(self, filename=""):
        try:
            with open(filename, 'r') as f:
                ulabox = json.load(f)
        except:
            print("The document '" + filename + "' is not available.\n")
            print("The scraper will retrieve all the products url.\n")
            # call to init scraper of url's
            ulabox = self.get_products()
            # get the dict/json urls
        else:
            print("The document '" + filename + "' is available.\n")
            print("Scraped url products loaded succesfuly.\n")

        # send the urls to the parser
        return ulabox

    def dataframe_to_csv(self, data):


        try:
            today = date.today().strftime("%b-%d-%Y")
            ruta = "../dataset/" + today + "_productes_alimentacio_ulabox.csv"
            data.to_csv(ruta, index=False, encoding='utf-8-sig')
        except Exception as ex:
            print(ex)
        print("Dataset created successfuly\n")
        return

    def scraper_get_all_products(self, dictionary_url):
        '''
        The scraper recieves the scraped url's, we parse the document and retrieve the information to finally create the dataset
        '''
        # Empty dataframe to store the scraped information of each products


        df_products = pd.DataFrame(columns=['Id', 'Categoria', 'Subcategoria', 'Enllaç',
                                            'Nom Producte', 'Preu', 'PreuBase', 'Ingredients',
                                            'Valor Energètic Kj', 'Valor Energetic KC', 'Greixos', 'Hidrats', 'Sucre',
                                            'Proteines', 'Sal',
                                            'Fabricant'])

        # Loop for retrieving and sraping each product
        id = 0
        for category in dictionary_url:
            for subcategory in dictionary_url[category]:
                for productsUrl in dictionary_url[category][subcategory]:
                    # getting the url of the product
                    print("Enllaç complet al producte: ", self.baseUrl + productsUrl)
                    product_link = self.baseUrl + productsUrl

                    # getting the soup and the product information
                    soup = self.scraper_get_soup(product_link)
                    product_info = self.scraper_get_products(soup, id, category, subcategory)

                    # Adding the product to the dataframe
                    df_products = df_products.append(product_info, ignore_index=True)
                    print("Added product\n\n")

                    # Product control for ID's and time.sleep
                    id = id + 1
                    # time.sleep()



        # Saving the results of all products
        self.dataframe_to_csv(df_products)
        return

    def scraper_get_soup(self, url):

        UserAgent = ({'User-Agent':
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                      'Accept-Language': 'en-US, en;q=0.5'})
        web = requests.get(url, headers=UserAgent)
        soup = BeautifulSoup(web.content, 'html.parser')

        return soup

    def get_new_product(self, id, category, subcategory):

        product = {
            'Id': id,
            'Categoria': category,
            'Subcategoria': subcategory,
            'Enllaç': "Not Available",
            'Nom Producte': "Not Available",
            'Preu': "Not Available",
            'PreuBase': "Not Available",
            'Ingredients': "Not Available",
            'Valor Energètic Kj': "Not Available",
            'Valor Energètic KC': "Not Available",
            'Greixos': "Not Available",
            'Hidrats': "Not Available",
            'Sucre': "Not Available",
            'Proteines': "Not Available",
            'Sal': "Not Available",
            'Fabricant': "Not Available"
        }

        return product

    def scraper_get_product_title(self, soup, product):
        try:
            name = soup.find("h1").get_text()
            product.update({'Nom Producte': name})
        except:
            print("Product name not found\n")

        return product

    def scraper_get_product_link(self, soup, product):
        try:
            link_soup = soup.find('link', {'href': True, 'rel': 'canonical'})
            link = link_soup['href']
            product.update({'Enllaç': link})
        except:
            print("Product link not found\n")

        return product

    def scraper_get_product_price(self, soup, product):
        try:
            price_soup = soup.find("meta", {'itemprop': 'price'})
            price = price_soup['content']
            product.update({'Preu': price})
        except:
            print("Product price not found\n")

        return product

    def scraper_get_product_base_price(self, soup, product):
        try:

            classFilter = ["jss470"]

            subpreu = soup.find_all("p")
            basePrice = ""

            for preustotals in subpreu:
                if preustotals['class'][1] in classFilter:
                    if basePrice != "":
                        basePrice = basePrice + " " + preustotals.text
                    else:
                        basePrice = preustotals.text

            product.update({'PreuBase': basePrice})

        except:
            print("Product base price not found\n")

        return product

    def scraper_get_product_nutritional_table(self, soup, product):
        '''
        The nutritional table may be found in ¿different layouts?:
        - Catalan titles
        - Spanish titles
        ¿english titles?
        '''
        try:

            titols = soup.find_all("h6")
            apartatsText = [
                "Description",
                "Ingredients",
                "Usage and preservation",
                "Additional information"
            ]
            # Get divs for the table content
            apartatsTaules = [
                "Nutrients",
                "Measures"
            ]

            divs = {}
            results = {}
            valors_nutricionals = []
            for titol in titols:
                if (titol.text in apartatsText):
                    divs[titol.text] = titol.find_next('div')
                    results[titol.text] = divs[titol.text].text

                if (titol.text in apartatsTaules):
                    for sibling in titol.find_next_siblings():
                        # Eliminem el text que no ens interesa
                        # From: 'Energetic valueAprox.3700 KJ' to -> 3700
                        valor_nutricional_numeric = sibling.text
                        valors_nutricionals.append(re.search(r'\d+', valor_nutricional_numeric).group())

            product.update({'Valor Energètic Kj': valors_nutricionals[0]})
            product.update({'Valor Energètic KC': valors_nutricionals[1]})
            product.update({'Greixos': valors_nutricionals[2]})
            product.update({'Hidrats': valors_nutricionals[3]})
            product.update({'Sucre': valors_nutricionals[4]})
            product.update({'Proteines': valors_nutricionals[5]})
            product.update({'Sal': valors_nutricionals[6]})

        except:
            print("Product nutritional table not found\n")

        return product

    def scraper_get_product_factory(self, soup, product):
        try:
            titols = soup.find_all("h6")
            apartatsText = [
                "Additional information"
            ]

            divs = {}
            results = {}
            valors_nutricionals = []
            for titol in titols:
                if (titol.text in apartatsText):
                    divs[titol.text] = titol.find_next('div')
                    results[titol.text] = divs[titol.text].text
                    factory = re.split(": ", results[titol.text])[1]

            product.update({'Fabricant': factory})

        except:
            print("Product factory name not found\n")

        return product

    def scraper_get_products_ingredients(self, soup, product):
        try:
            titols = soup.find_all("h6")
            apartatsText = [
                "Ingredients"
            ]

            divs = {}
            results = {}
            valors_nutricionals = []
            for titol in titols:
                if (titol.text in apartatsText):
                    divs[titol.text] = titol.find_next('div')
                    results[titol.text] = divs[titol.text].text
                    ingredients = results[titol.text]
                    ingredients = ingredients.replace("\n"," ")

            product.update({'Ingredients': ingredients})

        except:
            print("Product ingredients not found\n")

        return product

    def scraper_get_product_image(self, soup, id):
        try:

            image_html = soup.find("img", {'itemprop': 'image'})
            image_url = image_html['src']

            r = requests.get(image_url, stream=True)
            if r.status_code == 200:
                aSplit = image_url.split('.')
                ruta = "../imgs/" + str(id) +"."+ aSplit[-1]
                with open(ruta, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                return ruta
        except Exception as ex:
            print(ex)
            print("Product image not found\n")
        return

    def scraper_get_products(self, soup, id, category, subcategory):

        # Create an empty product
        product = self.get_new_product(id, category, subcategory)

        # Retrieve information and storage in the product
        product = self.scraper_get_product_title(soup, product)
        product = self.scraper_get_product_link(soup, product)
        product = self.scraper_get_product_price(soup, product)
        product = self.scraper_get_product_base_price(soup, product)
        product = self.scraper_get_product_nutritional_table(soup, product)
        product = self.scraper_get_product_factory(soup, product)
        product = self.scraper_get_products_ingredients(soup, product)

        self.scraper_get_product_image(soup, id)
        return product



a = UlaboxScrapper()
# print(a.get_products())

dictionary_url = a.scraper_web("producsdfsftsUrls.json")
a.scraper_get_all_products(dictionary_url)
