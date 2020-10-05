import requests
from authentication_twil import yelpHeaders
from pprint import pprint

# takes in a zip code as string, array of 20 places to call


def getpizzeria(zip_code):
    yelpParams = {
        'term': 'food',
        'location': zip_code,
        'categories': 'pizza',
        'open_now': True,
        'sort_by': 'rating'
    }

    yelpSearch = 'https://api.yelp.com/v3/businesses/search'
    foodResponse = requests.get(
        yelpSearch, headers=yelpHeaders, params=yelpParams)
    businesses = foodResponse.json()['businesses']
    # pprint(businesses)
    whitepages = {}
    for business in businesses:
        whitepages.update({business['name']: business['phone']})
    # convers dictionary to list that was sorted by rating to retain rating and access best first
    array = []
    for key, value in whitepages.items():
        temp = [key, value]
        array.append(temp)

    pprint(whitepages)
    pprint(array)
    print('This will be called:', array[0][0])
    return array
