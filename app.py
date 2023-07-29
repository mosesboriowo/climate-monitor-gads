#GADS Individual Project by Damilola Olaide Banjoko

#Climate Change Monitor to measure effect of air pollution data on climate change and increase awareness of environmental pollution globally

#This project uses the OpenWeather API to measure the current air pollution data based on the user's specified location and informs or recommmends appropriate action based on the retrieved Air Quality Index 


#env for the location and climate // pip install geopy && pip install meteostat && pip install requests
#Install Python 3.6 or higher 




from os import statvfs_result

from flask import Flask, jsonify, request, session, render_template, url_for, redirect, flash
from prometheus_client import Counter, start_http_server
from logging import Logger
import json, requests
import http.client
from logging import Logger
from datetime import datetime
from werkzeug.exceptions import abort

from geopy.geocoders import Nominatim #importing a py geolocation library

geofinder = Nominatim(user_agent="app") # initializing the library
current_city = ""
location = ""
longitude = ""
latitude =""

app = Flask(__name__) 

my_secrets = "749aac8ebf3b78c243ee7b994b4ca6aa"

# setting up redis as db
#app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
#redis_client = redis.from_url(app.config['REDIS_URL'])

# Define a Prometheus Counter
requests_counter = Counter('http_requests_total', 'Total HTTP requests')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/main', methods=('GET', 'POST'))
def main():
	if request.method == 'POST':
		global current_city	
		
		state = request.form['state']
		app.logger.debug(str(state))
		
		current_city = state
		app.logger.debug('POST method reached successfully')
		print(state)

		if len(current_city) == 0:
			app.logger.debug('One or more required fields is missing')
			flash('One or more required fields is missing')
		
		else:
			
			app.logger.debug('POST method executed successfully')
			return redirect(url_for('result'))
	else:
		app.logger.debug('GET method executed successfully')
	
	return render_template('main.html')
	
@app.route('/air_index.html')
def result():
	global current_city
	if current_city is None:
		return render_template('404.html'), 404

	else:
		entry = '"'+ str(current_city)+'"'
		app.logger.debug(entry)
		
		try:
			global location
			global longitude
			global latitude
			location = geofinder.geocode(entry, timeout=10000)
			longitude = location.longitude
			latitude = location.latitude 
		except:
			return render_template('404.html'), 404
		
		
		
		lon = str(longitude)
		print(lon)
		
		lat = str(latitude)
		print(lat)
		
			
		response = requests.get("https://api.openweathermap.org/data/2.5/air_pollution?lat="+ lat + "&lon=" + lon + "&appid=YOUR-KEY-HERE")
		pollution_index = json.loads(response.text)
		
		print(pollution_index)
		
		print(pollution_index['list'][0]['main']['aqi']) 
		
		result = pollution_index['list'][0]['main']['aqi']
		
		msg = None
		
		if result == 1:
			msg = 'Ideal: The Air Pollution Index is low at your location'
			app.logger.debug(msg)
			app.logger.debug('Ideal: The Air Pollution Index is low at your location')
		elif result == 2:
			msg = 'Fair:The Air Pollution is minimal at your location'
			app.logger.debug('Fair:The Air Pollution is average at your location')
			app.logger.debug(result)
		elif result == 3:
			msg = 'Moderate: The Air Pollution Index is a bit high, take precaution'
			app.logger.debug(result)
			app.logger.debug('Warning:The Air Pollution is Moderate at your location')
		elif result == 4:
			msg = 'Poor: The Air Pollution Index is very high, take precaution'
			app.logger.debug(result)
			app.logger.debug('At Risk: The Air Pollution Index is very high, take precaution')
		else:
			msg = 'Emergency: The Air Pollution Index is extreme today. Report status to appropriate local authorities'
			app.logger.debug(result)
			app.logger.debug('Emergency: The Air Pollution Index is extreme today. Report status to appropriate local authorities')
			

	
		return render_template('result.html', msg = msg)
	
def apply_security_configurations():
    with open('security.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


if __name__ == "__main__": 
	app.run(host='0.0.0.0', port=80, debug=True)
 
start_http_server(8000)
