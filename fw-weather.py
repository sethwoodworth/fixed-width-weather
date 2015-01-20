#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A python script for delivering the weather in a fixed number of characters.
Used in fixed-width terminal
Usage:
    fw-weather.py <citystate>
"""
from __future__ import print_function
from __future__ import unicode_literals
import datetime

from docopt import docopt
import requests


weather_symbols = {
    u'Clear': '☉',
    u'black_sun': '☀',
    u'cloud': '☁',
    u'some_cloud': '⛅',
    u'rain': '☔',
    u'rain_cloud': '⛈',
    u'thunderstorm': '☈',
    u'asc': '☊',
    u'desc': '☋',
    u'degree': '°'
}


class WeatherReport(object):
    """ A report of the weather
        takes: str 'city', 'state'
        makes an API call to openweathermap
    """
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q='
    api_options = '&units=imperial'

    def __init__(self, citystate):
        self.created_at = datetime.datetime.utcnow()
        self.citystate = citystate
        self.data = self._get_weather_data()
        self._parse_weather_data()

    def _get_weather_data(self):
        query_url = '{0}{1}{2}'.format(
            self.api_url,
            self.citystate,
            self.api_options)
        return requests.get(query_url).json()

    def _parse_weather_data(self):
        """ set weather values we want to use on self """
        self.temp_f = int(round(self.data['main']['temp']))
        self.desc = self.data['weather'][0]['description'].lower()

    def __str__(self):
        return "WeatherReport at now {0}".format(self.data)


def format_weather(weather, width=10):
    """ weather data formatter"""
    temp = '{0}{1}'.format(weather.temp_f, weather_symbols['degree'])
    weather_str = weather.data['weather'][0]['main']
    prompt = '{icon} {text} {temp}'.format(
        icon=weather_symbols[weather_str],
        text=weather_str,
        temp=temp)
    return prompt


def main(citystate):
    """ main repr function """
    global weather
    weather = WeatherReport(citystate)
    print(format_weather(weather))

import pprint
pp = pprint.PrettyPrinter()

if __name__ == '__main__':
    arguments = docopt(__doc__)

    citystate = arguments['<citystate>']
    main(citystate)
