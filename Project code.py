from gtts import gTTS
import test3
import speech_recognition as sr
import os
import re
import requests
import webbrowser
import smtplib
from datetime import time
from datetime import datetime
from datetime import date


def talkToMe(audio):
    tts = gTTS(text=audio, lang='en-uk')
    tts.save('audio.mp3')
    os.system('start audio.mp3')
    

def myCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print('You said: ' + command + '\n')

    except sr.UnknownValueError:
        talkToMe('Your last command couldn\'t be heard')
        command = myCommand()

    return command


def assistant(command):
    if 'open Reva' in command:
        talkToMe('Opening reva webpage')
        url = 'https://www.reva.edu.in/'
        webbrowser.open(url)
        print('Done!')

    elif 'website' in command:
        reg_ex = re.search('website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
            talkToMe('Opening your requested website')
        else:
            pass
    elif 'Google search' in command:
        new = 2
        talkToMe('what would you like searching for?')
        keyword = myCommand()
        url = "https://google.com/?#q="
        webbrowser.open(url+keyword,new=new)
        talkToMe('Here are some results for your request')
    elif 'open Notepad' in command:
        os.system("start notepad.exe")
        talkToMe("Opening notepad")
    elif 'open calculator' in command:
        os.system("start calc.exe")
        talkToMe("opening calculator")
    elif 'open Chrome' in command:
        os.system("start chrome.exe")
        talkToMe("opening google chrome")
    elif 'time' in command:
        now = datetime.time(datetime.now())
        print("Current time : ",now.strftime("%I:%M %p"))
        talkToMe(now.strftime("%I:%M %p"))
    elif 'date' in command:
        now = datetime.now()
        print("Current time : ",now.strftime("%d %B %y"))
        talkToMe(now.strftime("%d %B %y"))
    elif 'what\'s up' in command:
        talkToMe('Just doing my thing')
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            print(str(res.json()['joke']))
            talkToMe(str(res.json()['joke']))
        else:
            print('oops!I ran out of jokes')
            talkToMe('oops!I ran out of jokes')
    elif 'close' in command:
        if 'Chrome' in command:
            app = "chrome.exe"
            os.system("taskkill /f /im "+app)
            talkToMe('closing Chrome')
        
        elif 'notepad' in command:
            app = "notepad.exe"
            os.system("task'kill /f /im "+app)
            talkToMe('closing notepad')
        
    elif 'current temperature' in command:
        talkToMe("of which city?")
        city = myCommand();
        api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
        url = api_address + city
        json_data = requests.get(url).json()
        temp = json_data['main']['temp']
        tempinc = int(temp - 273.15)
        print('Current temperature in ' + city + ' : ' + str(tempinc) + ' celsius')
        talkToMe('current temperature in '+ city +' is '+ str(tempinc) +' degree celsius')
    elif 'email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()
        
        if 'Bharat' in recipient:
            talkToMe('What should I say?')
            content = myCommand()
            server = smtplib.SMTP('smtp.gmail.com', 468)
            server.ehlo()
            server.starttls()
            server.login('','')
            server.sendmail('bharatjb0@gmail.com', 'bharatjb4@gmail.com', content)
            server.close()
            talkToMe('Email sent.')
        else:
            talkToMe('I don\'t know what you mean!')

talkToMe('how can i help you?')

while True:
    assistant(myCommand())
