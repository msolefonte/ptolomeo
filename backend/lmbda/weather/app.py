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


"""This is a sample for a weather fulfillment webhook for an Dialogflow agent
This is meant to be used with the sample weather agent for Dialogflow, located at
https://console.dialogflow.com/api-client/#/agent//prebuiltAgents/Weather
This sample uses the WWO Weather Forecast API and requires an WWO API key
Get a WWO API key here: https://developer.worldweatheronline.com/api/
"""

from lmbda.weather.forecast import Forecast, validate_params


def handler(event, context):

    # This check allows testing in AWS Lambda
    if 'body' in event:
        req = event['body']
    else:
        req = event

    fulfillment_text = make_response(req)

    response = {
        "fulfillmentText": fulfillment_text,
        "outputContexts": []
    }

    return response


def make_response(req):
    action = req['queryResult']['action']

    if action == 'weather':
        res = weather(req)
    elif action == 'weather.activity':
        res = weather_activity(req)
    elif action == 'weather.condition':
        res = weather_condition(req)
    elif action == 'weather.outfit':
        res = weather_outfit(req)
    elif action == 'weather.temperature':
        res = weather_temperature(req)
    else:
        raise NotImplementedError
    return res


def weather(req):
    """Returns a string containing text with a response to the user
    with the weather forecast or a prompt for more information
    Takes the city for the forecast and (optional) dates
    uses the template responses found in weather_responses.py as templates
    """

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(req['queryResult']['parameters'])
    if error:
        return error

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return str(error)

    # If the user requests a datetime period (a date/time range), get the
    # response
    if forecast.datetime_start and forecast.datetime_end:
        response = forecast.get_datetime_period_response()
    # If the user requests a specific datetime, get the response
    elif forecast.datetime_start:
        response = forecast.get_datetime_response()
    # If the user doesn't request a date in the request get current conditions
    else:
        response = forecast.get_current_response()

    return response


def weather_activity(req):
    """Returns a string containing text with a response to the user
    with a indication if the activity provided is appropriate for the
    current weather or a prompt for more information
    Takes a city, activity and (optional) dates
    uses the template responses found in weather_responses.py as templates
    and the activities listed in weather_entities.py
    """

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(req['queryResult']['parameters'])
    if error:
        return error

    # Check to make sure there is a activity, if not return an error
    if not forecast_params['activity']:
        return 'What activity were you thinking of doing?'

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    # get the response
    return forecast.get_activity_response()


def weather_condition(req):
    """Returns a string containing a human-readable response to the user
    with the probability of the provided weather condition occurring
    or a prompt for more information
    Takes a city, condition and (optional) dates
    uses the template responses found in weather_responses.py as templates
    and the conditions listed in weather_entities.py
    """

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(req['queryResult']['parameters'])
    if error:
        return error

    # Check to make sure there is a activity, if not return an error
    if not forecast_params['condition']:
        return 'What weather condition would you like to check?'

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    # get the response
    return forecast.get_condition_response()


def weather_outfit(req):
    """Returns a string containing text with a response to the user
    with a indication if the outfit provided is appropriate for the
    current weather or a prompt for more information
    Takes a city, outfit and (optional) dates
    uses the template responses found in weather_responses.py as templates
    and the outfits listed in weather_entities.py
    """

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(req['queryResult']['parameters'])
    if error:
        return error

    # Validate that there are the required parameters to retrieve a forecast
    if not forecast_params['outfit']:
        return 'What are you planning on wearing?'

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    return forecast.get_outfit_response()


def weather_temperature(req):
    """Returns a string containing text with a response to the user
    with a indication if temperature provided is consisting with the
    current weather or a prompt for more information
    Takes a city, temperature and (optional) dates.  Temperature ranges for
    hot, cold, chilly and warm can be configured in config.py
    uses the template responses found in weather_responses.py as templates
    """

    parameters = req['queryResult']['parameters']

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(parameters)
    if error:
        return error

    # If the user didn't specify a temperature, get the weather for them
    if 'temperature' not in forecast_params:
        return weather(req)

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    return forecast.get_temperature_response(forecast_params['temperature'])
