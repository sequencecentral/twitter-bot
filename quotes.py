import json
import random

def create_random_tweet():
    quote = get_random_quote()
    tweet = """{} 
            - {}""".format(quote['quoteText'], quote['quoteAuthor'])
    return tweet

def get_quotes():
    with open('quotes-list.json') as f:
        quotes_json = json.load(f)
    return quotes_json['quotes']

def get_random_quote():
    quotes = get_quotes()
    random_quote = random.choice(quotes)
    return random_quote