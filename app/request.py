import urllib.request,json

api_url=None

def create_configuration(app):
    global api_url
    api_url=app.config['RANDOM_API']

#create an api request
def get_quote():
    quote_api_url=api_url
    with urllib.request.urlopen(quote_api_url) as url:
        if url.getcode()==200:
            read_content=url.read()
            json_data=json.loads(read_content)
        else:
            print('The people who lead are not the smartest but the bold.')

    return json_data                