#!/usr/bin/env python
# kupi.cz web scraper for scraping recipes into JSON
import requests
from bs4 import BeautifulSoup
import json


class KupiRecipes:
    CATEGORIES = ('dezerty-a-sladka-jidla', 'hlavni-jidla', 'napoje',
                  'omacky-a-gulase', 'polevky', 'predkrmy-chutovky-a-svaciny',
                  'prilohy-pecivo', 'salaty', 'zavarovani-a-nakladani')
    def __init__(self):
        self.url = 'https://www.kupi.cz/recepty/'
        
    def get_categories(self):
        return self.CATEGORIES

    def __get_recipes(self, url, full=False, from_search=False):
        """
        Private method for scraping recipes from given url.

        Args:
            url (str): URL of page with recipes
            full (bool): If True, each recipe is fully scraped (all details of recipe are retrieved) and added to the output JSON. This increases output a lot. Defaults to False.
            from_search (bool): If True, the requests comes from search method (get recipes by search). Defaults to False.

        Returns:
            str: JSON string with list of dictionaries, each containing recipe info
        """
        response = requests.get(url)
        recipes = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            recipes = []
            page = 2
            
            # search (hledej) has different ending paragraph <p> class tag
            termination = soup.find('p', class_='content_p') if from_search else soup.find('p', class_='notfound')
            
            # goes through all pages of selected category and gets all recipes
            # end is indicated by presence of "notfound"
            while termination is None:
                
                recipes_list_div = soup.find_all('div', class_='recipes_list')            
                
                for r_list in recipes_list_div:
                
                    recipes_divs = r_list.find_all('div', class_='recipe_item')
                
                
                    for recipe in recipes_divs:
                        recipe_data = recipe.find('h2')
                        recipe_url = recipe_data.find('a').get('href')
                        
                        full_recipe = self.__get_recipe_detail(recipe_url) if full else None

                                                                
                        recipes.append({
                            'name': recipe_data.text.strip(),
                            'url': recipe_url,
                            'recipe': full_recipe
                        })
                            
                new_url = url + '&page=' + str(page) if from_search else url + '?page=' + str(page)
                response = requests.get(new_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                termination = soup.find('p', class_='content_p') if from_search else soup.find('p', class_='notfound')
                page += 1
                
            return json.dumps(recipes, ensure_ascii=False)
            
        else:
            return json.dumps([])
        
    
    
    def get_recipes_by_category(self, category, full=False):
        """
        Gets recipes by category.

        Args:
            category (str): The category name of the recipes to get.
            full (bool): If True, each recipe is fully scraped (all details of recipe are retrieved) and added to the output JSON. This increases output a lot. Defaults to False.

        Returns:
            str: A JSON string containing the recipes by category.
        """
        url = self.url + category        
        return self.__get_recipes(url, full)
        
    def get_all_recipes(self, full=False):
        """
        Gets all recipes from all categories.

        Args:
            full (bool): If True, each recipe is fully scraped (all details of recipe are retrieved) and added to the output JSON. This increases output a lot. Defaults to False.

        Returns:
             list: List of JSON strings containing the recipes by category.
        """
        recipes = []
        for category in self.CATEGORIES:
            recipes.append(self.get_recipes_by_category(category, full))
            
        return recipes
    
    def get_recipe_detail(self, recipe_url):
        """
        Gets detail of single recipe.

        Args:
            recipe_url (str): The URL of the recipe page.

        Returns:
            str: A JSON string containing the recipe detail.
        """
        return json.dumps(self.__get_recipe_detail(recipe_url), ensure_ascii=False)
    
    def __get_recipe_detail(self, recipe_url):
        """
        Private method for scraping details of single recipe.

        Args:
            recipe_url (str): The URL of the recipe page.

        Returns:
            dict: A dictionary containing the recipe detail. Is then proccessed into JSON.
        """
        recipe_response = requests.get(recipe_url)
        recipe_soup = BeautifulSoup(recipe_response.content, 'html.parser')
        
        # Name
        recipe_header = recipe_soup.find('div', class_='recipe_header')
        title = recipe_header.find('h1').text.strip()
        
        # Parameters
        parameters = recipe_soup.find('div', class_='parameters')
        try:
            time = parameters.find('div', class_='time').text.strip()
        except:
            time = None
        try:
            difficulty = parameters.find('div', class_='diff').text.strip()
        except:
            difficulty = None
        try:
            price = parameters.find('div', class_='price').text.strip()
        except:
            price = None    
        
        params = [time, difficulty, price]
        
        # Ingredients
        
        ingredients_box = recipe_soup.find('div', class_='ingredients_box')
        ingredients_list = ingredients_box.find_all('div', class_='ingredients_list--wrap')
        
        ingredients_parts = []
        for ingredient_element in ingredients_list:
            try:
                ingredient_element_name = ingredient_element.find('h3').text.strip()
            except:
                ingredient_element_name = title
                
            ingredient_elements_list = ingredient_element.find_all('li')
            
            ingredients = []
            for ingredient in ingredient_elements_list:
                ingredient_name_div = ingredient.find('div', class_='ingredient_name')
                ingredient_name = ingredient_name_div.text.strip()
                ingredient_url = ingredient_name_div.find('a').get('href')
                ingredient_amount = ingredient.find('div', class_='ingredient_amount').text.strip()
                ingredients.append({
                    'ingredient_name': ingredient_name,
                    'ingredient_url': ingredient_url,
                    'ingredient_amount': ingredient_amount
                })
            
            ingredients_parts.append({
                'recipe_part_name': ingredient_element_name,
                'ingredients': ingredients
            })
            
        # Instructions
        instructions_list = recipe_soup.find_all('div', class_='instructions_list--wrap')
        
        instructions_parts = []
        for instruction_element in instructions_list:
            try:
                instruction_element_name = instruction_element.find('h3').text.strip()
            except:
                instruction_element_name = title
            
            instruction_elements_list = instruction_element.find_all('li')
            instructions = []
            for instruction in instruction_elements_list:
                instruction_index = instruction.find('div', class_='instruction_index').text.strip()
                instruction_value = instruction.find('div', class_='instruction_value').text.strip()
                instructions.append({
                    'index': instruction_index,
                    'value': instruction_value
                })
            
            
            instructions_parts.append({
                'name': instruction_element_name,
                'instructions': instructions
            })
            
        recipe_data = {
            'title': title,
            'params': params,
            'ingredients': ingredients_parts,
            'instructions': instructions_parts
        }
            
        return recipe_data
    
    def get_recipe_by_search(self, search, full=False):
        """
        Gets recipes by search.

        Args:
            search (str): The search query to use to find the recipes.
            full (bool): If True, each recipe is fully scraped (all details of recipe are retrieved) and added to the output JSON. This increases output a lot. Defaults to False.

        Returns:
            str: A JSON string containing the recipes by search.
        """
        url = self.url + 'hledej?f=' + search
        # we need from_search flag because of diffent ending conditions
        return self.__get_recipes(url, full, from_search=True) 
        