import unittest
from kupi_api.scraper import KupiScraper
import json

class TestKupiScraper(unittest.TestCase):
    
    def setUp(self):
        self.kupi = KupiScraper()
        
    def test_search(self):
        print("Testing search")
        products = self.kupi.get_discounts_by_search('jogurt')
        print(products)
        print("#"*20)
        products =json.loads(products)
        product_names = [product['name'] for product in products]
        print(product_names)

        
    def test_category(self):
        print("Testing category")
        products = self.kupi.get_discounts_by_category('pivo')
        print(products)
        print("#"*20)
        
    def test_category_shop(self):
        print("Testing category and shop")
        products = self.kupi.get_discounts_by_category_shop('pivo', 'lidl')
        print(products)
        print("#"*20)
    
   
        
    def test_shop(self):
        print("Testing shop")
        products = self.kupi.get_discounts_by_shop('lidl')
        print(products)
        print("#"*20)
        

if __name__ == '__main__':
    unittest.main()
