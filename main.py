# -*- coding: utf-8 -*-
from textblob import TextBlob, exceptions
from flowlauncher import FlowLauncher

AUTOMATIC_LANGUAGES = 'cs'

def translate(query):
    query_modified = query.strip().lower()
    splitted = query_modified.split(' ')
    
    results = []
    if len(splitted) > 3:
        from_lang = splitted[0]
        to_lang = splitted[1]

        en = set(chr(i) for i in range(ord('a'), ord('z') + 1))
        
        if query_modified:
            try:
                blob = TextBlob(' '.join(splitted[2:]))
                translation = blob.translate(from_lang, to_lang)
                results.append({
                    "Title": str(translation),
                    "SubTitle": query,
                    "IcoPath":"Images/app.png"
                })
            except exceptions.NotTranslated:
                results.append({
                    "Title": 'Query not changed',
                    "SubTitle": query,
                    "IcoPath":"Images/app.png"
                })
    if not results:
        results.append({
                "Title": 'Not found',
                "SubTitle": query,
                "IcoPath":"Images/app.png"
            })
    return results

class Translate(FlowLauncher):
    
    def query(self, query):
        return translate(query)
        
    def context_menu(self, data):
        return []


if __name__ == "__main__":
    Translate()
