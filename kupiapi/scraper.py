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
        
    
    def __get_products_info(self, url, from_search=False):
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
            page = 2
            product_list = []
            
            # goes through pages of all products
            # terminates when there is no more pages of products
            while True:
                end = False
                products = soup.find_all('div', class_='group_discounts')
                for product in products:
                    name = product.find('div', class_='product_name')
                    name = name.find('strong').text.strip()
                                    
                    try:
                        discounts_table = product.find('table', class_='discounts_table')
                    except:
                        end = True
                        break
                    try:
                        shops = discounts_table.find_all('span', class_='discounts_shop_name')
                    except:
                        end = True
                        break
                    
                    product_data = discounts_table.find_all('tr', class_='discount_row')
                    
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
                            validities.append(self.clean_text(pd.find('td',class_='discounts_validity').text))
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
            
                new_url = url + '&page=' + str(page) if from_search else url + '?page=' + str(page)
                response = requests.get(new_url)
                
                if self.check_url(response.url) == False:
                    break
                
                print(response.url);
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page += 1
                    
            return json.dumps(product_list, ensure_ascii=False)
        else:
            return json.dumps([])
        

    
    def get_discounts_by_category(self, category):
        """
        Gets discounts by category.

        Args:
            category (str): The category name of the discounts to get.

        Returns:
            str: A JSON string containing the discounts by category.
        """
        url = self.url + '/slevy/' + category
        return self.__get_products_info(url)
        
    def get_discounts_by_search(self, search):
        """
        Gets discounts by search.

        Args:
            search (str): The search query to use to find the product.

        Returns:
            str: A JSON string containing the discounts by search.
        """
        
        url = self.url + '/hledej?f=' + search
        return self.__get_products_info(url, from_search=True)
        
    def get_discounts_by_shop(self, shop):
        """
        Gets discounts by shop.

        Args:
            shop (str): The shop name (e.g. Lidl) of the discounts to get.

        Returns:
            str: A JSON string containing the discounts by shop.
        """
        url = self.url + '/slevy/' + shop
        return self.__get_products_info(url)
       
        
    def get_discounts_by_category_shop(self, category, shop):
        """
        Gets discounts by category and shop.

        Args:
            category (str): The category name of the discounts to get.
            shop (str): The shop name (e.g. Lidl) of the discounts to get.

        Returns:
            str: A JSON string containing the discounts by category and shop.
        """
        url = self.url + '/slevy/' + category + '/' + shop
        return self.__get_products_info(url)


    