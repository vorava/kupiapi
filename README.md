# Kupi API

This is a lightweight *www.kupi.cz* web scraper for scraping **sales** and **recipes** into JSON. It requires only bs4, json and requests libraries. API provides multiple methods to download content (recipes and discounts) from the **kupi** website (see more below).

There are two main parts (classes). **KupiScraper** for scraping data about sales and **KupiRecipes** for downloading recipes that are published on kupi.cz. Output of methods from this library can be further use in machine-processable tasks.

## Instalation via pip
    pip install kupiapi

PyPi page of the library: [https://pypi.org/project/kupiapi/](https://pypi.org/project/kupiapi/)

GitHub page of the library: [https://github.com/vorava/kupiapi](https://github.com/vorava/kupiapi)

## Usage
    import kupiapi.scraper # imports KupiScraper() class
    import kupiapi.recipes # imports KupiRecipes() class
    

## Methods - Kupi scraper
All methods return JSON formated data if not declared elsewise. All methods have parameter *max_pages*, which sets how many pages of discount should be scraped. Default values is 0, that means "scrape all pages".

    get_discounts_by_category(category, max_pages=0)

As parameter takes name of the category as string value. Scrapes data from this category. Discounts are scraped from url kupi.cz/slevy/**category**. List of main categories can be obtained by method *get_categories()*.

    get_discounts_by_search(search, max_pages=0)

Scrapes discounts by search. Search can be any string. This method searches only discounted goods (by adding tag *&vse=0* in the url string).

    get_discounts_by_shop(shop, max_pages=0)

Returns discounts from specific shop, defined by *shop* argument.

    get_discounts_by_category_shop(category, shop, max_pages=0)

Combines search by shop name and by category.

    get_categories()

Returns list of main categories, that can be used in method *get_discounts_by_category(category, max_pages=0)*



## Methods - Kupi repices
All methods return JSON formatted data. Parameter *full* is boolean. If true full recipe info is scrapped (size of the output is significantly bigger).

    get_recipes_by_category(category, full=False):

Scrapes recipes by given category (string value). Categories can be obrained by calling method *get_categories()*.

    get_all_recipes(full=False):

Scrapes all recipes available at kupi.cz.

    get_recipe_by_search(search, full=False)

Gets recipe by string *search*.

    get_recipe_detail(recipe_url):

Gets detail of recipe by url (string value). Its mandatory to provide correct url addres of recipe.

    get_categories()

Returns all possible categories of recipes.



## Examples
    import kupiapi.recipes
    kr = kupiapi.recipes.KupiRecipes()
    
    print(kr.get_categories())
----

    import kupiapi.scraper
    import kupiapi.recipes

    sc = kupiapi.scraper.KupiScraper()
    rc = kupiapi.recipes.KupiRecipes()

    print(sc.get_discounts_by_search('pivo'))
    print(rc.get_recipes_by_category('hlavni-jidla',full=False))
    