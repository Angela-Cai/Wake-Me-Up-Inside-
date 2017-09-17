# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 17:06:14 2017

@author: Angela and Isabelle
"""
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import urllib
import datetime
import json, requests
import random
#import pygame
import time

#from gpiozero import Button
#from gpiozero import LED
from time import sleep

"""def flash(flash_on):
	led = LED(27) #3 is the GPIO pin no
	off_button = Button(17) #2 is the GPIO pin linked to the button

	while True:
		try off_button.is_pressed:
			break
		except KeyboardInterrupt:
			GPIO.cleanup()
		led.on(0.5)
		sleep(0.5)
		led.off(0.5)
		sleep(0.5)
	GPIO.cleanup()


def play_sound(sound_name):
	off_button = Button(17) #2 is the GPIO pin linked to the button
	pygame.mixer.init()
	song = pygame.mixer.music.load("~/%s" % sound_name)
	song.play()
	off_button.when_pressed = song.stop()"""

def test_print(to_print):
	i = 0
	while i < 5:
		print(datetime.datetime.utcnow())
		time.sleep(3)
		i+=1

#type_options = {"song1":play_sound,"song2":play_sound,"song3":play_sound,"flash":flash,"vibrate":vibrate}
type_options = {"test":test_print}

def chose_alarm_type():
	type_options_names = ["test"]
	#type_options_names = ["song1","song2","song3","buzz","vibrate"]
	return random.choice(type_options_names)


def is_it_time(alarm_time,alarm_type):
	current_time = datetime.datetime.utcnow()
	str_current_time = "%s/%s/%s,%s:%s" % (current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)
	str_alarm_time = "%s/%s/%s,%s:%s" % (alarm_time.year, alarm_time.month, alarm_time.day, alarm_time.hour, alarm_time.minute)

	while True:
		current_time = datetime.datetime.utcnow()
		str_current_time = "%s/%s/%s,%s:%s" % (current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)

		if str_current_time == str_alarm_time:
			break

	type_options[alarm_type](alarm_type)
	print("alarm off")

	"""ANGELA"""

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def set_alarm(user_override = None):
    if (not(user_override is None)):
        return user_override

    (first_event_time_wrong_format, location) = main()
    year = int(first_event_time_wrong_format[0:4])
    month = int(first_event_time_wrong_format[5:7])
    day = int(first_event_time_wrong_format[8:10])
    day = 17
    hour = (int(first_event_time_wrong_format[11:13]) - int(first_event_time_wrong_format[19:22])) % 24
    hour = 15
    minute = int(first_event_time_wrong_format[14:16])
    minute = 20
    second = int(first_event_time_wrong_format[17:19])
    first_event_time = datetime.datetime(year, month, day, hour, minute, second)

    travel_time = calculate_time(first_event_time, location)
    prep_time = datetime.timedelta(minutes=travel_time + 30)
    print(first_event_time - prep_time)
    return first_event_time - prep_time
    
def calculate_time(first_event_time, location):
    ip = "10.189.21.204"
    #IP2LocObj = IP2Location.IP2Location()
    #IP2LocObj.open("data/IP-COUNTRY-REGION-CITY-LATITUTE-LONGITUDE-ZIPCODE-TIMEZONE-ISP-DOMAIN-NETSPEED-AREACODE-WEATHER-MOBILE-ELEVATION-USAGETYPE-SAMPLE.BIN")
    #rec = IP2LocObj.get_all("10.189.21.204")
    #start_place = str(rec.latitude + ',' + rec.longitude)
    start_place = "42.365079,-71.104519"
    
    location_matrix = location.split()
    end_place = ''
    for e in location_matrix:
        end_place += str(e) + '+'
    end_place = end_place[0:len(end_place)-1]
    span = first_event_time - datetime.datetime(1970,1,1,0,0,0)
    departure_time = span.days*24*3600 + span.seconds
    
    time_tree = requests.get("https://maps.googleapis.com/maps/api/directions/json?origin=" + start_place + "&destination=" + end_place + "&departure_time=" + str(departure_time) + "&key=AIzaSyATSYUkUn-CBHRCSvG3ie8V9rxs1e-H4HU")
    tree = json.loads(time_tree.text)
    route = tree["routes"][0]
    travel_time = 0
   
    for leg in route['legs']:
        for step in leg['steps']:
            travel_time += int(step['duration']['text'].split()[0])
    return travel_time

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            flags.auth_host_port =[8010, 8020]
            credentials = tools.run_flow(flow, store, flags)
#        else: # Needed only for compatibility with Python 2.6
#            credentials = tools.run(flow, store)
#        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming event')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=1, singleEvents=True).execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        location = event['location']
        return (start, location)


set_own_alarm = input("Do you want to set your own alarm? (y/n)")
if set_own_alarm == "y":
	input("What time do you want to set? ")
alarm_time = set_alarm()
is_it_time(alarm_time, chose_alarm_type())
