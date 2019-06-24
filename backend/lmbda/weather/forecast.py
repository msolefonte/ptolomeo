# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module that defines the Forecast class and defines helper functions to
process and validate date related to the weather forecast class

This is meant to be used with the sample weather agent for Dialogflow, located at
https://console.dialogflow.com/api-client/#/agent//prebuiltAgents/Weather

This sample uses the WWO Weather Forecast API and requires an WWO API key
Get a WWO API key here: https://developer.worldweatheronline.com/api/
"""

import random
from datetime import datetime as dt
from datetime import timedelta
from dateutil.parser import parse
from botocore.vendored import requests
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

from .config import (_TEMP_LIMITS, _DEFAULT_TEMP_UNIT, _DEFAULT_LOCATION, WWO_API_KEY,
                     WWO_LANGUAGE, MAX_FORECAST_LEN)
from .weather_responses import (
    LIST_YES,
    LIST_NO,
    LIST_COLD,
    LIST_CHILLY,
    LIST_WARM,
    LIST_HOT,
    WEATHER_CURRENT,
    WEATHER_DATE,
    WEATHER_WEEKDAY,
    WEATHER_DATE_TIME,
    WEATHER_TIME_PERIOD,
    WEATHER_TIME_PERIOD_DEFINED,
    WEATHER_DATE_PERIOD_WEEKEND,
    WEATHER_DATE_PERIOD,
    WEATHER_ACTIVITY_YES,
    WEATHER_ACTIVITY_NO,
    RESPONSE_WEATHER_CONDITION,
    RESPONSE_WEATHER_OUTFIT)
from .weather_entities import (WINTER_ACTIVITY, SUMMER_ACTIVITY, DEMI_ACTIVITY,
                               CONDITION_DICT, UNSUPPORTED, COLD_WEATHER,
                               WARM_WEATHER, HOT_WEATHER, RAIN, SNOW, SUN)


class Forecast(object):
    """The Forecast object implements tracking of and forecast retrieval for
    a request for a weather forecast.  Several methods return various human
    readable strings that contain the weather forecast, condition, temperature
    and the appropriateness of outfits and activities to for forecasted weather

    This requires setting the WWO_API_KEY constant in config.py to a string
    with a valid WWO API key for retrieving weather forecasts

    Attributes:
        city (str): the city for the weather forecast
        datetime_start (datetime.datetime): forecast start date or datetime
        datetime_end (datetime.datetime): forecast end date or datetime
        unit (str): the unit of temperature: Celsius ('C') or Fahrenheit ('F')
        action (dict): any actions in the request (activity, condition, outfit)
        forecast (dict): structure containing the weather forecast from WWO
    """

    def __init__(self, params):
        """Initializes the Forecast object

        gets the forecast for the provided dates
        """

        self.city = params['city']
        self.datetime_start = params['datetime_start']
        self.datetime_end = params['datetime_end']
        self.unit = params['unit']
        self.action = {
            'activity': params['activity'],
            'condition': params['condition'],
            'outfit': params['outfit'],
        }

        self.forecast = self.__get_forecast()

    def __get_forecast(self):
        """Takes a date or date period and a city

        raises an exception when dates are outside what can be forecasted
        Returns the weather for the period and city as a dict
        """

        datetime_start = self.datetime_start
        datetime_end = self.datetime_end

        if datetime_start and datetime_end:
            date_interval = datetime_end - datetime_start
            forecast_length = date_interval.days
        elif datetime_start:
            forecast_length = 1
        else:
            datetime_start = dt.now().date()
            forecast_length = 1

        # Get the start date
        try:
            date_start = datetime_start.date()
        except AttributeError:
            date_start = datetime_start

        # Get the furthest date in the future we can get a forecast for
        max_forecast_date = dt.now().date() + timedelta(days=MAX_FORECAST_LEN)
        furthest_date_requested = date_start + timedelta(days=forecast_length)

        # Check to see that the forecast dates requested are not too far into
        # the future
        if furthest_date_requested > max_forecast_date:
            raise ValueError(
                'Lo siento. No puedo encontrar un pronóstico tan lejano.')

        # Get the weather for each day (each needs a separate API call)
        for day in range(forecast_length):
            current_date = date_start + timedelta(days=day)

            response = self.__call_wwo_api(current_date.strftime('%Y-%m-%d'))

            try:
                forecast['weather'].append(response['weather'][0])
            except NameError:
                forecast = response

        return forecast

    def __call_wwo_api(self, date):
        """Calls the wwo weather API for a date

        raises an exception for network errors
        Returns a dict of the JSON 'data' attribute in the response
        """

        wwo_data = {
            'key': WWO_API_KEY,
            'q': self.city,
            'format': 'json',
            'num_of_days': 1,
            'mca': 'no',
            'lang': WWO_LANGUAGE,
            'cc': 'yes',
            'tp': '1',
            'fx': 'yes',
            'date': date
        }

        response = requests.get(
            'http://api.worldweatheronline.com/premium/v1/weather.ashx',
            params=wwo_data
        )

        weather_data = response.json()['data']
        error = weather_data.get('error')
        if error:
            raise IOError(error[0]['msg'])
        else:
            return weather_data

    def __get_max_min_temp(self):
        """Calculate the max and min temperatures for the date range
        """

        temps = []
        for day in self.forecast['weather']:
            for hour in day['hourly']:
                temps.append(int(hour['temp' + self.unit]))

        return max(temps), min(temps)

    def get_datetime_response(self):
        """Takes a datetime and forecast

        Returns the forecast for that datetime as a string
        """

        max_temp = int(self.forecast['weather'][0]['maxtemp' + self.unit])
        min_temp = int(self.forecast['weather'][0]['mintemp' + self.unit])
        temp = (max_temp + min_temp) / 2
        temperature = str(temp).encode('utf-8') + u'°'.encode('utf-8') + self.unit.encode('utf-8')
        condition = self.forecast['weather'][0]['hourly'][
            12]['lang_es'][0]['value'].lower()

        # Get the start date
        try:
            date_start = self.datetime_start.date()
        except AttributeError:
            date_start = self.datetime_start

        # if the weather forecast is for today and they specified a time
        if (date_start == dt.now().date() and
                isinstance(self.datetime_start, dt)):
            output_string = random.choice(WEATHER_DATE_TIME)
            response = output_string.format(
                place=self.city,
                time=self.datetime_start.strftime('%I:%M%p'),
                temperature=temperature.decode(),
                condition=fix_weather(condition),
                day='Hoy')
        # else
        else:
            # if it's within a week
            time_difference = date_start - dt.now().date()
            if time_difference <= timedelta(days=7):
                # Get the day of the week or set to 'today'
                day = 'El ' + self.datetime_start.strftime('%A')
                if date_start == dt.now().date():
                    day = 'Hoy'
                # Format Response
                output_string = random.choice(WEATHER_DATE)
                response = output_string.format(
                    place=self.city,
                    day=day,
                    temperature=temperature.decode(),
                    condition=fix_weather(condition))
            # if the date is more than a week away
            else:
                output_string = random.choice(WEATHER_WEEKDAY)
                response = output_string.format(
                    place=self.city,
                    condition=fix_weather(condition),
                    temperature=temperature.decode(),
                    date=self.datetime_start.strftime('%B %-d'))
        return response

    def get_datetime_period_response(self):
        """Takes a date period and forecast

        Returns the forecast for the date period as a string
        """

        datetime_start = self.datetime_start
        datetime_end = self.datetime_end
        forecast = self.forecast

        # datetime period over the same day
        if datetime_start.day == datetime_end.day:

            # Get the temperature throughout the time period and average it
            temps = []
            hours = []
            # Get the set of hours in military time to average over for the day
            for hour in range(datetime_start.hour, datetime_end.hour + 1):
                hours.append(str(hour * 100))  # WWO API uses military time
            # Get the forecasted temperature for every hour during the period
            for hour in forecast['weather'][0]['hourly']:
                if hour['time'] in hours:
                    temps.append(hour['temp' + self.unit])
            # Calculate the average temperature for the time period
            avg_temp = sum(temps) / len(temps)
            # Make a human readable string of the temperature
            temperature = str(avg_temp) + str(u'°'.encode('utf-8')) + self.unit

            # Get the conditions for the time period
            condition = forecast['weather'][0]['hourly'][
                datetime_start.hour + 1]['lang_es'][0]['value'].lower()

            # Choose the right word to describe the time period
            if datetime_start.hour <= 12 and datetime_end.hour <= 16:
                time_period = 'afternoon'
            elif datetime_start.hour <= 0 and datetime_end.hour <= 8:
                time_period = 'night'
            elif datetime_start.hour <= 16 and datetime_end.hour <= 23:
                time_period = 'tonight'
            else:
                time_period = 'morning'

            # if the time period can be described with a word use it here
            if time_period:
                output_string = random.choice(
                    WEATHER_TIME_PERIOD_DEFINED)
                response = output_string.format(
                    place=self.city,
                    time_period=time_period,
                    temperature=temperature.decode(),
                    condition=fix_weather(condition))

            # If the time period cannot be defined by a single word use the
            # time the user provided
            else:
                output_string = random.choice(WEATHER_TIME_PERIOD)
                response = output_string.format(
                    condition=fix_weather(condition),
                    city=self.city,
                    temp=temperature,
                    time_start=datetime_start.strftime('%I:%M%p'),
                    time_end=datetime_end.strftime('%I:%M%p'))

        # datetime period over multiple days
        else:
            # If the user is requesting weather for the weekend
            if datetime_start.day == 5 and datetime_end.day == 6:
                response = random.choice(WEATHER_DATE_PERIOD_WEEKEND).format(
                    city=self.city,
                    condition_sun=forecast['weather'][1]['hourly'][
                        12]['lang_es'][0]['value'].lower(),
                    sun_temp_min=forecast['weather'][1]['mintemp' + self.unit],
                    sun_temp_max=forecast['weather'][1]['maxtemp' + self.unit],
                    condition_sat=forecast['weather'][0]['hourly'][
                        12]['lang_es'][0]['value'].lower(),
                    sat_temp_min=forecast['weather'][0]['mintemp' + self.unit],
                    sat_temp_max=forecast['weather'][0]['maxtemp' + self.unit])
            # If the user is requesting a non-weekend date range
            else:
                (max_temp, min_temp) = self.__get_max_min_temp()

                # Format temperature strings
                max_temp = str(max_temp).encode('utf-8') + u'°'.encode('utf-8') + self.unit.encode('utf-8')
                min_temp = str(min_temp).encode('utf-8') + u'°'.encode('utf-8') + self.unit.encode('utf-8')

                response = random.choice(WEATHER_DATE_PERIOD).format(
                    date_start=datetime_start.strftime('%Y-%m-%d'),
                    date_end=datetime_end.strftime('%Y-%m-%d'),
                    city=self.city,
                    condition=forecast['weather'][0]['hourly'][
                        12]['lang_es'][0]['value'].lower(),
                    degree_list_min=min_temp,
                    degree_list_max=max_temp)

        return response

    def get_activity_response(self):
        """Takes an activity and a forecast

        returns the appropriateness of activity with the weather as a string
        """

        activity = self.action['activity']
        (max_temp, _) = self.__get_max_min_temp()

        if activity in DEMI_ACTIVITY:
            resp = random.choice(WEATHER_ACTIVITY_YES)
        elif activity in WINTER_ACTIVITY:
            if max_temp <= _TEMP_LIMITS['cold'][self.unit]:
                resp = random.choice(WEATHER_ACTIVITY_YES)
            else:
                resp = random.choice(WEATHER_ACTIVITY_NO)
        elif activity in SUMMER_ACTIVITY:
            if max_temp >= _TEMP_LIMITS['warm'][self.unit]:
                resp = random.choice(WEATHER_ACTIVITY_YES)
            else:
                resp = random.choice(WEATHER_ACTIVITY_NO)
        else:
            resp = 'I don\'t know about %s' % activity

        return resp

    def get_condition_response(self):
        """Takes a condition and returns the probability as a string
        """

        condition = self.action['condition']

        if condition in CONDITION_DICT.keys():
            condition_chance = self.forecast['weather'][
                0]['hourly'][12][CONDITION_DICT[condition]]
            resp = random.choice(RESPONSE_WEATHER_CONDITION).format(
                condition_original=translate_condition(condition),
                condition=condition_chance
            )
        else:
            resp = 'I don\'t know about %s' % condition

        return resp

    def get_outfit_response(self):
        """Takes an outfit and a forecast

        returns the appropriateness of outfit with the weather as a string
        """

        outfit = self.action['outfit']
        (max_temp, min_temp) = self.__get_max_min_temp()
        condition_chance = None

        if outfit in COLD_WEATHER:
            condition = 'haga frío'
            answer = LIST_YES if min_temp < _TEMP_LIMITS[
                'chilly'][self.unit] else LIST_NO
        elif outfit in WARM_WEATHER:
            condition = 'se esté bien'
            answer = LIST_YES if max_temp < _TEMP_LIMITS[
                'warm'][self.unit] else LIST_NO
        elif outfit in HOT_WEATHER:
            condition = 'haga calor'
            answer = LIST_YES if max_temp < _TEMP_LIMITS[
                'hot'][self.unit] else LIST_NO
        elif outfit in RAIN:
            condition = 'llueva'
            condition_chance = self.forecast['weather'][
                0]['hourly'][12]['chanceofrain']
            answer = LIST_YES if int(condition_chance) < 50 else LIST_NO
        elif outfit in SNOW:
            condition = 'nieve'
            condition_chance = self.forecast['weather'][
                0]['hourly'][12]['chanceofsnow']
            answer = LIST_YES if int(condition_chance) < 50 else LIST_NO
        elif outfit in SUN:
            condition = 'haga sol'
            condition_chance = self.forecast['weather'][
                0]['hourly'][12]['chanceofsunshine']
            answer = LIST_YES if int(condition_chance) > 50 else LIST_NO
        else:
            return 'I don\'t know about %s' % outfit

        if condition_chance:
            return random.choice(RESPONSE_WEATHER_OUTFIT).format(
                condition_original=translate_condition(condition),
                condition=condition_chance,
                answer=random.choice(answer))
        else:
            return random.choice(answer)

    def get_temperature_response(self, target_temperature):
        """Takes a temperature and indicates its severity in a string
        """

        header = "Sí. "
        temp = int(self.forecast['current_condition'][0]['temp_' + self.unit])

        if temp >= _TEMP_LIMITS['hot'][self.unit]:
            if target_temperature is 'cold':
                header = 'No. '
            resp = LIST_HOT
        elif temp > _TEMP_LIMITS['chilly'][self.unit]:
            if target_temperature is 'cold':
                header = 'No. '
            resp = LIST_WARM
        elif temp > _TEMP_LIMITS['cold'][self.unit]:
            if target_temperature is 'hot':
                header = 'No. '
            resp = LIST_CHILLY
        else:
            if target_temperature is 'hot':
                header = 'No. '
            resp = LIST_COLD

        return header + random.choice(resp)

    def get_current_response(self):
        """Takes a forecast and returns the current conditions as a string
        """

        # Get the temperature by average the high and low for the day
        temp = self.forecast['current_condition'][0]['temp_' + self.unit]
        temperature = temp.encode(
            'utf-8') + u'°'.encode('utf-8') + self.unit.encode('utf-8')

        # Get the conditions in the middle of the day
        condition = self.forecast['weather'][0][
            'hourly'][12]['lang_es'][0]['value'].lower()

        output_string = random.choice(WEATHER_CURRENT)

        return output_string.format(
            place=self.city,
            temperature=temperature.decode(),
            condition=fix_weather(condition)
        )


def validate_params(parameters):
    """Takes a list of parameters from a HTTP request and validates them

    Returns a string of errors (or empty string) and a list of params
    """

    # Initialize error and params
    error_response = ''
    params = {}

    # City
    if (parameters.get('address') and
            isinstance(parameters.get('address'), dict)):
        params['city'] = parameters.get('address').get('city')
    else:
        params['city'] = _DEFAULT_LOCATION

    # Date-time
    datetime_input = None
    if parameters.get('date-time'):
        if parameters.get('date-time'):
            datetime_input = parameters.get('date-time')

    datetime_start, datetime_end = parse_datetime_input(datetime_input)
    params['datetime_start'] = datetime_start
    params['datetime_end'] = datetime_end

    # Unit
    params['unit'] = parameters.get('unit')
    if not params['unit'] and _DEFAULT_TEMP_UNIT:
        params['unit'] = _DEFAULT_TEMP_UNIT

    # activity
    if parameters.get('activity'):
        activity = parameters.get('activity')
        if (activity not in SUMMER_ACTIVITY and
                activity not in WINTER_ACTIVITY and
                activity not in DEMI_ACTIVITY):
            error_response += 'unknown activity '
    params['activity'] = parameters.get('activity')

    # condition
    params['condition'] = parameters.get('condition')
    if params['condition'] in UNSUPPORTED:
        error_response += 'unsupported condition '

    # outfit
    params['outfit'] = parameters.get('outfit')

    # Special parameters
    # activity
    params['activity'] = parameters.get('activity')

    # condition
    params['condition'] = parameters.get('condition')

    # temperature
    params['temperature'] = parameters.get('temperature')

    return error_response.strip(), params


def parse_datetime_input(datetime_input):
    """Takes a string containing date/time and intervals in ISO-8601 format

    Returns a start and end Python datetime.datetime object
    datetimes are None if the string is not a date/time
    datetime_end is None if the string is not a date/time interval
    """

    datetime_end = None
    if datetime_input:
        if 'endDate' in datetime_input:
            datetime_end = parse(datetime_input['endDate'])
            datetime_start = parse(datetime_input['startDate'])
        elif 'dateTime' in datetime_input:
            datetime_start = parse(datetime_input['dateTime'])
        else:
            datetime_start = parse(datetime_input)
    else:
        datetime_start = None

    return datetime_start, datetime_end


def translate_condition(condition):
    en = ['rain', 'snow', 'wind', 'sun', 'shower', 'fog', 'ice', 'thunderstorm',
            'freezing rain', 'rain snow', 'haze', 'overcast', 'clouds', 'foggy',
            'showers', 'hurricane']
    es = ['llueva', 'nieve', 'haga viento', 'haga sol', 'mojarse', 'haya niebla',
               'haya hielo', 'haya tormenta', 'granice', 'nieve', 'haya niebla',
               'haya nubes', 'haya nubes', 'haya niebla', 'haya chubascos', 'haya un huracán']

    for i in range(len(en)):
        if condition == en[i]:
            return es[i]
    return condition


def fix_weather(weather):
    error = ['parcialmente nublado']
    patch = ['cielo parcialmente nublado']
    for i in range(len(error)):
        if weather == error[i]:
            return patch[i]
    return weather
