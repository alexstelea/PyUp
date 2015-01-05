PyUp
===========
The most comprehensive Python Jawbone UP API wrapper.


Installation
------------

Import the UPAPI class from the PyUp file

`from PyUp import UpAPI`

Initialize the UPAPI object to any variable

`jawbone = UPAPI()`

Usage
-----

##Band Events 

`data = jawbone.get_band_events(access_token, date=None, start_time=None, end_time=None, created_after=None)`

##Goals 

###Get Goal

`data = jawbone.get_user_goals(access_token)`   

###Set Goal

`jawbone.set_user_goal(access_token, move_steps=None, sleep_total=None, body_weight=None, body_weight_intent=None)`

## Heartrate



Requirements
------------

This wrapper only needs the following two requirements:

`urllib` and `requests` 