import json
import random

def create_random_tweet():
    quote = quotes.get_random_quote()
    tweet = """
            {}
            ~{}
            """.format(quote['quote'], quote['character'])
    return tweet

def get_quotes():
    with open('data.json') as f:
        quotes_json = json.load(f)
    return quotes_json['quotes']

def get_random_quote():
    quotes = get_quotes()
    random_quote = random.choice(quotes)
    return random_quote