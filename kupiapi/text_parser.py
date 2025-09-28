#!/usr/bin/env python
# supporting class for kupi scraper
class TextParser:
    def __init__(self):
        pass
    
    def clean_text(self, text_to_clean):
        """
        Clean text by removing leading and trailing whitespace, replacing 
        non-breaking space by normal space and removing linebreaks. Also 
        remove leading slash if present.
        
        Args:
            text_to_clean (str): The string to clean.
        
        Returns:
            str: The cleaned string.
        """
       
        output_text = text_to_clean.replace(u'\xa0', ' ').replace(u'\n', '').strip()
        output_text = ' '.join(output_text.split()) # remove multiple spaces
        if output_text[0] == '/':
            output_text = output_text[1:].strip()
            
        return output_text
    
    def check_url(self, url):
        """
        Check if the given URL contains a query string.
        
        Args:
            url (str): The URL to check.
        
        Returns:
            bool: True if the URL contains a query string, False otherwise.
        """
        if '&' in url or '?' in url:
            return True
        return False