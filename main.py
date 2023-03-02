#import libraries
import json
from datetime import datetime, date
import urllib.parse
import urllib.request

def weather(request):
  #get json format of request
  request_json = request.get_json()
  #retrieve city name and date
  city_name = request_json['sessionInfo']['parameters']['location_city']
  query_date = request_json['sessionInfo']['parameters']['date']

  #transform date to appropiate format
  query_date = date(query_date['year'], query_date['month'], query_date['day'])

  api_key = "**************"
  endpoint = 'https://api.openweathermap.org/data/2.5/forecast'
  #complete_url = base_url + "APPID=" + api_key + "&q=" + city_name
  #specify parameters for query
  query_params = {
    'q': city_name,
    'appid': api_key
    }
  #encode query parameters
  query_string = urllib.parse.urlencode(query_params)
  #send API request and retrieve JSON response
  response = urllib.request.urlopen(endpoint + '?' + query_string)
  weather_data = json.loads(response.read().decode())
  
  #send API request and retrieve JSON response
  # response = requests.get(endpoint, params=query_params)
  # weather_data = response.json()
  
  #if x.get("code") == 200: Error handling
  #collect neccessary forecast data
  forecast_data = []
  #fill dicts with data
  for forecast in weather_data['list']:
    forecast_date = datetime.fromtimestamp(forecast['dt'])
    forecast_time = forecast['dt_txt'].split()[1]
    forecast_temp_min = forecast['main']['temp_min']
    forecast_temp_max = forecast['main']['temp_max']
    forecast_data.append({'date': forecast_date, 'time': forecast_time, 'temp_min': forecast_temp_min, 'temp_max': forecast_temp_max})

  #collect all the minimum and maximum temperatures of day
  min_temps = []
  max_temps = []
  for datestamp in forecast_data:
    #check data of day
    if datestamp['date'].date() == query_date:
      min_temps.append(datestamp['temp_min'])
      max_temps.append(datestamp['temp_max'])

  #calculate the minimum and maximum temperature of day
  min_temp = min(min_temps)
  max_temp = max(max_temps)
  #create response text
  response_text = "On " + str(date) + " in " + city_name + " the minimum temperature is " + str(min_temp) + "°C and the maximum temperature is " + str(max_temp) + "°C"
  #dump minimum and maximum temperatures in appropiate json format
  return json.dumps(
        {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [f"Minimum temperature: {min_temp} Maximum temperature: {max_temp}"],
                            "allow_playback_interruption": False,
                        }
                    }
                ]
            }
        }
    )
  #else: #error handling
  #  response_text = "Sorry, I could not find the weather information for " + city_name
  #  return {"fulfillmentText": response_text}
