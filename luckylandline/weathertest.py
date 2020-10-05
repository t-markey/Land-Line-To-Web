from pprint import pprint
import requests
from authentication_twil import weather_key
# _____________________________________________________________Testing city

# takes in a string and outputs a string


def gettingWeather(city_name):
    API_key = weather_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    Final_url = base_url + "appid=" + API_key + "&q=" + city_name

    weather_data = requests.get(Final_url).json()
    # Error handling of an unrecognized city name
    try:
        # Accessing Description, it resides in weather and its key is description
        description = weather_data['weather'][0]['description']
        # Accessing Temperature, temperature resides in main and its key is temp
        tempKel = weather_data['main']['temp']
        # gives temp in fahrenheit
        tempFar = str(int(((tempKel - 273.15)*1.8)+32))

        print("\nCurrent Weather Data Of " + city_name + ":\n")
        pprint(weather_data)
        outputWeather = 'The weather in ' + city_name + \
            ' is '+description+' and ' + tempFar+' degrees'
        # print('\n\n\n'+outputWeather)
        return outputWeather
    except KeyError:
        return 'try to say another city name'


# _____________________________________________________________Notes
# This is the full base url to work from .
# http://api.openweathermap.org/data/2.5/weather?appid=YOUR API KEY&q=Delhi


# print(gettingWeather('denning'))
