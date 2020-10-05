from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial
from twilio.twiml.messaging_response import MessagingResponse, Message
import wikipedia as wk
from authentication_twil import account_sid, auth_token, from_
from twilio.rest import Client
import random
import weathertest
import pizzatest


app = Flask(__name__)
choice = 3
client = Client(account_sid, auth_token)
# _____________________________________________________________MAIN MENU


@app.route("/", methods=['GET', 'POST'])
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()

    # get input
    with resp.gather(numDigits=1, action='/gather') as gather:
        gather.say('To gather information Press 1.  To get your local weather forcast, press 2. To be connected to a local pizzeria, Press 3. To send a text messege, Press 4.')

    # if no selection, restart menu
    resp.redirect('/voice')

    return str(resp)


@app.route('/gather', methods=['GET', 'POST'])
def gather():
    # sort out <gather> responses from voice
    resp = VoiceResponse()

    # process input
    if 'Digits' in request.values:
        # gets input
        choice = request.values['Digits']

        if choice == '1':
            resp.say('You requested Information')
            resp.redirect('/infoing')
        elif choice == '2':
            resp.say('You requested a Weather forcast.')
            resp.redirect('/weathering')
        elif choice == '3':
            resp.say('You must be hungry.')
            resp.redirect('/pizza')
        elif choice == '4':
            resp.say('You wanted to send a text messege.')
            print(choice)
            resp.redirect('/texting')
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, Choose one of the other available options")

    # if no selection return to main menu

    resp.redirect('/voice')
    return str(resp)

# _____________________________________________________________Handles #4 texting info


@app.route('/texting', methods=['GET', 'POST'])
def texting():
    global choice
    print('wierd')
    print(choice)
    resp = VoiceResponse()
    # get input
    with resp.gather(numDigits=10, timeout='6', action='/storing') as gather:
        gather.say('Input the number you wish to text')
        print('wierd')
        print(choice)
    # all the shit in this function gets run before the input....?
    resp.redirect('/voice')
    return str(resp)


@app.route('/storing', methods=['GET', 'POST'])
def storing():
    resp = VoiceResponse()
    global choice
    print('wierd4')
    choice = 333333
    print(choice)
    if 'Digits' in request.values:
        choice = request.values['Digits']
        print(choice)

    resp.redirect('/speeching')
    return str(resp)


@app.route('/speeching', methods=['GET', 'POST'])
def speeching():
    global choice
    if 'Digits' in request.values:
        choice = request.values['Digits']
        print(choice)

    resp = VoiceResponse()
    resp.say('Say your messege aloud')
    gather = Gather(input='speech', timeout=3,
                    hints='yes, no', action='/texting2')
    resp.append(gather)
    resp.redirect('/voice')
    return str(resp)


# SEND SMS HERE
@app.route('/texting2', methods=['GET', 'POST'])
def texting2():
    resp = VoiceResponse()
    # takes input from last function
    if 'SpeechResult' in request.values:
        infoo = request.values['SpeechResult']
    print(choice, "IN THE RIGHT SPOT")
    finishedNumber = '+1' + choice
    # sends text from voice from this number to number user inputs
    message = client.messages.create(
        body=infoo,
        from_=from_,
        to=finishedNumber)
    resp.say('Your Text message has been sent')
    resp.redirect('/voice')
    return str(resp)
# _____________________________________________________________Handles #1 wiki info


@ app.route('/infoing', methods=['GET', 'POST'])
def infoing():
    global infoo

    resp = VoiceResponse()
    resp.say('Say a topic you would like to learn about')
    # This sends speech to inforouting 2 to be sorted out
    gather = Gather(input='speech', speechTimeout=1,
                    hints='yes, no', action='/infoing2')
    resp.append(gather)
    resp.say('I didnt quite get that')
    resp.redirect('/infoing')
    return str(resp)


@ app.route('/infoing2', methods=['GET', 'POST'])
def infoing2():
    global infoo
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        infoo = request.values['SpeechResult']
        print('this is testing: ', infoo)
        # fixes an issue where wiki api gets error
        try:
            p = wk.summary(infoo)
            print('p:', p)
        except wk.DisambiguationError as e:
            s = random.choice(e.options)
            print('s:', s)
            p = wk.summary(s)
            print('p2:', p)

        cut = p

        # checks to make sure summary is not bigger than 3000 char limit
        # MAKE IT SOIGNE SPLIT THE SUMMARY INTO TWO SAYS TO USE WHOLE SUMMARY
        if len(cut) > 3000:
            resp.say(cut[0:2800])
        else:
            resp.say(cut)

    else:
        resp.say('I didnt quite get that')

    resp.redirect('/infoing')
    return str(resp)
# _____________________________________________________________Handles #3 Pizza
# setup infrastuctre, get location, get dominos


@app.route('/pizza', methods=['GET', 'POST'])
def pizza():
    resp = VoiceResponse()
    # get zip and city
    zips = request.values['FromZip']
    city = request.values['FromCity']
    print('Your zip code is {}'.format(zips))
    pizzaArray = pizzatest.getpizzeria(zips)
    resp.say('I will be connecting you to {} near, {}.'.format(
        pizzaArray[0][0], city))
    # dials the pizzeria
    resp.dial(pizzaArray[0][1])
    resp.say('Goodbye')

    resp.redirect('/voice')
    return str(resp)


# _____________________________________________________________Handles #2 Weather
@app.route('/weathering', methods=['GET', 'POST'])
def weathering():
    resp = VoiceResponse()
    # get city and output weather:
    city = request.values['FromCity']
    print('User location : {}.'.format(city))
    resp.say(weathertest.gettingWeather(city))
    resp.say('If you would like to get the weather of another city , say it now')

    # ask user if they would like to get weather for another city
    gather = Gather(input='speech', speechTimeout=3, action='/otherweathering')
    resp.append(gather)

    resp.redirect('/voice')
    return str(resp)


@app.route('/otherweathering', methods=['GET', 'POST'])
def otherweathering():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        city = request.values['SpeechResult']
        print('User location : {}.'.format(city))
        resp.say(weathertest.gettingWeather(city))
        # redirects to get user info again
        if weathertest.gettingWeather(city) == 'try to say another city name':
            resp.redirect('/otherweathering2')
    resp.redirect('/voice')
    return str(resp)

# little redirect back to processing user input for city input


@app.route('/otherweathering2', methods=['GET', 'POST'])
def otherweathering2():
    resp = VoiceResponse()
    gather = Gather(input='speech', speechTimeout=3, action='/otherweathering')
    resp.append(gather)
    # if no input, go back to main menu
    resp.redirect('/voice')
    return str(resp)


# _____________________________________________________________
if __name__ == "__main__":
    app.run(debug=True)
