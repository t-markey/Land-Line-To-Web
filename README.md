# Land Line to Web

A fun & useful information line for those without access to the internet 

# Features
* Say a topic and have that topics wikipedia article's summary read to you
* Receive local or another region'ss current weather forcast
* Be connected to the highest rated and currently open local pizzeria
* Input a phone number and say a text message to be sent

## Examples
[Link To Video Example](https://twitter.com/tommarkey5/status/1317531049820303361)
![gif](/luckylandline/examples/landline2web.gif)


## Installation

1. See the [twilio ](https://www.twilio.com/docs/voice) Documentation for getting started.

2. Getting your local host set up with ngrok:

```bash
cd path_to_ngrok
```
Make this executable on mac:

```bash
chmod +x ./ngrok
```
3. In a separate terminal window from your virtual environment run:

```bash
./ngrok http 5000
```
4. In your virtual environment run:

```bash
python3 dtmf.py
```
to start your flask server.



## Usage
There is some credentials required to get this all up and running
```python
#in dtmf.py Twilio Keys and phone number registered with them
from authentication_twil import account_sid, auth_token, from_
...
 #in weathertest.py API key from openweather
from authentication_twil import weather_key

#in pizzatest.py Yelp API credentials
from authentication_twil import yelpHeaders

```





## Credits
https://pypi.org/project/Wikipedia-API/

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
