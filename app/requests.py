import urllib, json
from .models import Quote

base_url = 'http://quotes.stormconsultancy.co.uk/random.json'


def get_quote():
    with urllib.request.urlopen(base_url) as url:
        response_data = url.read()
        response = json.loads(response_data)

        author = response['author']
        quote = response['quote']

        quote_object = Quote( author, quote)

    return quote_object