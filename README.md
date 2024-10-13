# Kupi API

This is a lightweight *www.kupi.cz* web scraper for scraping **sales** and **recipes** into JSON. It does require only bs4, json and requests libraries. API provides multiple methods to download content from the kupi website (see more below).

## Instalation
> pip install kupiapi

PyPi page: [https://pypi.org/project/kupiapi/](https://pypi.org/project/kupiapi/)

GitHub page: [https://github.com/vorava/kupiapi](https://github.com/vorava/kupiapi)

## Usage
    import kupiapi.recipes
    import kupiapi.scraper


## Examples
    import kupiapi.recipes
    kr = kupiapi.recipes.KupiRecipes()
    
    print(kr.get_categories())