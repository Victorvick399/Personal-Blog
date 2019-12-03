import urllib.request,json
from .models import Quote

base_url=None

def configure_request(app):
  global base_url

  base_url=app.config["BASE_URL"]

def get_quotes():
  '''
  function that gets the json response from the base url
  '''
  with urllib.request.urlopen(base_url) as url:
    data=url.read()
    print('********************here************************')
    print(data)
    response=json.loads(data)
    
    results=process_quote(response)

  return results

def process_quote(item):
  '''
  function that processes the response from json format
  '''
  results=[]
  print('************************ONA HAHA**********************')
  print(results)
  author=item.get('author')
  quote=item.get('quote')

  quote_object=Quote(author,quote)
  results.append(quote_object)

  return results 