#!/usr/bin/env python
# kupi.cz web scraper for scraping sales into JSON
import requests
from bs4 import BeautifulSoup
from kupiapi.text_parser import TextParser
import json

class KupiScraper:
    def __init__(self):
        self.url = 'https://www.kupi.cz'
        self.text_parser = TextParser()
        self.clean_text = self.text_parser.clean_text
        self.check_url = self.text_parser.check_url
        
    
    def __get_products_info(self, url:str, from_search:bool=False, max_pages:int=5):
        """
        Private method for scraping products from given url.

        Args:
            url (str): URL of page with products
            from_search (bool): If True, the requests comes from search method (get discounts by search). Defaults to False.

        Returns:
            str: JSON string with list of dictionaries, each containing product info
        """
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page = 1
            product_list = []
            end = False
            
            # goes through pages of all products
            # terminates when there is no more pages of products
            while not(end):
                products = soup.find_all('div', class_='group_discounts')
                if products == []:
                    end = True
                    break
    
                for product in products:
                    name = product.find('div', class_='product_name')
                    name = name.find('strong').text.strip()
                                    
                    try:
                        discounts_table = product.find('div', class_='discounts_table')
                    except:
                        end = True
                        break
                    try:
                        shops = discounts_table.find_all('span', class_='discounts_shop_name')
                    except:
                        end = True
                        break
                    
                    product_data = discounts_table.find_all('div', class_='discount_row')
                    
                    
                    # data about product (price, amount, discount validity)
                    prices = []
                    amounts = []
                    validities = []
                    for pd in product_data:
                        
                        try:
                            prices.append(self.clean_text(pd.find(class_='discount_price_value').text))
                        except:
                            prices.append(None)
                        
                        try:
                            amounts.append(self.clean_text(pd.find(class_='discount_amount').text))
                        except:
                            amounts.append(None)
                            
                        try:
                            validities.append(self.clean_text(pd.find('div',class_='discounts_validity').text))
                        except:
                            validities.append(None)
                                                                                
                    product_list.append({
                        'name': name,
                        'shops': [self.clean_text(shop.text) for shop in shops],
                        'prices': prices,
                        'amounts': amounts,
                        'validities': validities
                    })
                    
                if end:
                    break
            
                if max_pages != 0:
                    if page >= max_pages:
                        end = True
                        break
                
                page += 1
                new_url = url + '&page=' + str(page) if from_search else url + '?page=' + str(page)
                #print(new_url)
                response = requests.get(new_url)
                
                if self.check_url(response.url) == False:
                    end = True
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')                            
                
                
                    
            return json.dumps(product_list, ensure_ascii=False)
        else:
            return json.dumps([])
        

    
    def get_discounts_by_category(self, category:str, max_pages:int=0):
        """
        Gets discounts by category.

        Args:
            category (str): The category name of the discounts to get.
            max_pages (int): The maximum number of pages to scrape. Defaults to 0 (means all pages).

        Returns:
            str: A JSON string containing the discounts by category.
        """
        url = self.url + '/slevy/' + category
        return self.__get_products_info(url, max_pages=max_pages)
        
    def get_discounts_by_search(self, search:str, max_pages:int=0):
        """
        Gets discounts by search.

        Args:
            search (str): The search query to use to find the product.
            max_pages (int): The maximum number of pages to scrape. Defaults to 0 (means all pages).

        Returns:
            str: A JSON string containing the discounts by search.
        """
        
        url = self.url + '/hledej?f=' + search + "&vse=0" #vse=0 means only discounts
        return self.__get_products_info(url, from_search=True, max_pages=max_pages)
        
    def get_discounts_by_shop(self, shop:str, max_pages:int=0):
        """
        Gets discounts by shop.

        Args:
            shop (str): The shop name (e.g. Lidl) of the discounts to get.
            max_pages (int): The maximum number of pages to scrape. Defaults to 0 (means all pages).

        Returns:
            str: A JSON string containing the discounts by shop.
        """
        url = self.url + '/slevy/' + shop
        return self.__get_products_info(url, max_pages=max_pages)
       
        
    def get_discounts_by_category_shop(self, category:str, shop:str, max_pages:int=0):
        """
        Gets discounts by category and shop.

        Args:
            category (str): The category name of the discounts to get.
            shop (str): The shop name (e.g. Lidl) of the discounts to get.
            max_pages (int): The maximum number of pages to scrape. Defaults to 0 (means all pages).

        Returns:
            str: A JSON string containing the discounts by category and shop.
        """
        url = self.url + '/slevy/' + category + '/' + shop
        return self.__get_products_info(url, max_pages=max_pages)
    
    def get_categories(self):
        response = requests.get('https://www.kupi.cz/slevy')

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            categories_div = soup.find('div', class_='categories')
            
            categories_a = categories_div.find_all('a', class_='category_item')
            
            categories = [self.clean_text(c['href']).split('/')[-1] for c in categories_a]
            
            return json.dumps(categories)
            
        else:
            return json.dumps([])


    