import time
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager




class UlaboxScrapper:

    def __init__(self):
        self.url = "https://www.ulabox.com/ca/categoria/alimentacio/895?ula_src=&ula_mdm=header_bar&ula_cmp=main_category"
        self.baseUrl = "https://www.ulabox.com"
        self.browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

    def __get_soup(self, url):
        print(url)
        soup = self.__get_soup_from_url(url)
        while soup is None:
            print("ERROR")
            time.sleep(1)
            soup = self.__get_soup_from_url(url)
        return soup

    def __get_soup_from_url(self, url):
        try:
            self.browser.get(url)
            time.sleep(1)
            html = self.browser.page_source
        except WebDriverException:
            print("error")
            return None
        soup = BeautifulSoup(html, "lxml")
        return soup

    def __get_all_categories_urls(self, url ):
        soup = self.__get_soup(url)
        menuCategories = soup.find('ul', attrs={'class': "MuiList-root MuiList-dense MuiList-padding"})
        categories = {}
        for categoria in menuCategories.findAll('li'):
            elemA = categoria.find('a')
            url = elemA['href']
            text = elemA.get_text().strip()
            categories[text]=url
        return categories



    def __get_all_subcategories_urls(self):
        categories = self.__get_all_categories_urls(self.url)
        for categoria in categories:
            print("categoria")
            print(categories[categoria])
            categories[categoria]=self.__get_all_categories_urls(self.baseUrl+categories[categoria])
        return categories

    def __get_subcategory_products(self, url):
        print("subcategoria")
        soup = self.__get_soup(url)


        productes = set()
        elemsA = soup.findAll('a')
        for elem in elemsA:
            if elem.has_attr('href'):
                enllac = elem['href']
                if 'producte' in enllac:
                    productes.add(enllac)

        nextPage = soup.find('a', attrs={"rel": 'next'})
        if len(productes)==60 and nextPage:
            productes = productes.union(self.__get_subcategory_products(self.baseUrl+nextPage['href']))
        return productes

    def get_products(self):
        urls = self.__get_all_subcategories_urls()
        for categoria in urls:
            for subcategoria in urls[categoria]:
                urls[categoria][subcategoria] = self.__get_subcategory_products(self.baseUrl+urls[categoria][subcategoria])

        return urls

    def __del__(self):
        self.browser.close()

a = UlaboxScrapper()
print(a.get_products())

