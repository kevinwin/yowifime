# -*- coding: utf-8 -*-
"""
Yo single tap wifi recommendation
Yo Docs: http://docs.justyo.co
Yo Keys: http://dev.justyo.co
Yelp code from https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py
Yelp Docs: http://www.yelp.com/developers/documentation
Yelp Keys: http://www.yelp.com/developers/manage_api_keys
"""
import sys
import requests
import oauth2
import rauth
from flask import request, Flask

API_HOST = 'api.yelp.com'
SEARCH_LIMIT = 1

# Yo API Token: http://dev.justyo.co
YO_API_TOKEN = '6cce4bc4-5151-42f9-8e94-d81fc5389617'

def do_request(params):
  #Obtain these from Yelp's manage access page
  consumer_key = "3J0vOb8Pkm0ZVj6RNT6SgQ"
  consumer_secret = "9PCim5pcmDmHAUFtqPQlFwfitRg"
  token = "WqA1ClKuVKCjalKpcD_93c0vXRWEBxD7"
  token_secret = "c7PZFWyW173hCwGj28u0KhaXoH0"
  print params 
  session = rauth.OAuth1Session(
    consumer_key = consumer_key
    ,consumer_secret = consumer_secret
    ,access_token = token
    ,access_token_secret = token_secret)
     
  request = session.get("http://api.yelp.com/v2/search",params=params)

   
  #Transforms the JSON API response into a Python dictionary
  data = request.json()
  session.close()
   
  return data    


def search(city, latitude, longitude):
    
    params = {}
    params["term"] = "wifi"
    params["location"] = city
    params["cll"] = "{},{}".format(str(latitude),str(longitude))
    params["radius_filter"] = "1600"
    params["limit"] = SEARCH_LIMIT
    params["sort"] = 2


    return do_request(params)


app = Flask(__name__)


@app.route("/yo/")
def yo():

    # extract and parse query parameters
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]

    print "We got a Yo from " + username

    # get the city name since Yelp api must be provided with at least a city even though we give it accurate coordinates
    response = requests.get('http://nominatim.openstreetmap.org/reverse?format=json&lat=' + latitude + '&lon=' +longitude + '&zoom=18&addressdetails=1')
    response_object = response.json()
    city = response_object['address']['city']

    print username + " is at " + city

    # search for wifi spots using Yelp api
    response = search(city, latitude, longitude)
    print response

    # grab the first result
    wifi_place = response['businesses'][0]

    print wifi_place
    wifi_place_url = wifi_place['mobile_url']

    print "Recommended wifi spot is " + wifi_place['name']

    # Yo the result back to the user
    requests.post("http://api.justyo.co/yo/", data={'api_token': YO_API_TOKEN, 'username': username, 'link': wifi_place_url})

 
    return 'OK'


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)