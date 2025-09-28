import unittest
import sys
sys.path.append('../')
from kupiapi.recipes import KupiRecipes

class TestKupiScraper(unittest.TestCase):
    
    def setUp(self):
        self.kupi = KupiRecipes()
    
    def test_scrape_kupi_products(self):
        print("Testing getting recipes by category zavarovani-a-nakladani")
        recipes = self.kupi.get_recipes_by_category('zavarovani-a-nakladani')
        print(recipes)
        print(len(recipes))
        print("#" *20)
        
    def test_get_all(self):
        print("Testing getting all recipes")
        recipes = self.kupi.get_all_recipes()
        print(recipes)
        print(len(recipes))
        
    def test_recipe(self):
        print("Testing getting recipe detail")
        recipe = self.kupi.get_recipe_detail('https://www.kupi.cz/recepty/recept/4764-dynove-placky-s-kremovym-dipem')
        print(recipe)
        print("#" *20)
        
    def test_search(self):
        print("Testing search of pernik with full=True")
        recipes = self.kupi.get_recipe_by_search('pernik', full=True)
        print(recipes)
        print(len(recipes))
        print("#" *20)
        
        
        

if __name__ == '__main__':
    unittest.main()
