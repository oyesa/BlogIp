import request

# function to get quote from API
def get_quotes():
    response = request.get('http://quotes.stormconsultancy.co.uk/random.json')
    if response.status_code == 200:
        quote = response.json()
        return quote