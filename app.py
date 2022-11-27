#GADS Individual Project by Damilola Olaide Banjoko

#Climate Change Monitor to measure effect of air pollution data on climate change and increase awareness of environmental pollution globally

#This project uses a CNN API to measure the current air pollution data based on the user's specified location and informs or recommmends appropriate action based on the retrieved Air Quality Index 


#env for the location and climate // pip install geopy && pip install meteostat 
#Install Python 3.6 or higher 

from os import statvfs_result

from flask import Flask, jsonify, request, session, render_template, url_for, redirect, flash
from logging import Logger
import json
import http.client
from logging import Logger
from datetime import datetime
from werkzeug.exceptions import abort

from geopy.geocoders import Nominatim #importing a py geolocation library

geofinder = Nominatim(user_agent="app") # initializing the library


app = Flask(__name__) 

app.secret_key = your-key-here

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/main', methods=('GET', 'POST'))
def main():
	if request.method == 'POST':
		app.logger.debug('POST method executed successfully')
		user = request.form['name']
		state = request.form['state']

		#session['state'] = request.form['state']
		#app.logger.debug('POST method executed successfully')
		if not user and state:
			flash('One or more required fields is missing')
		else:
			return redirect(url_for('result'))
	else:
		app.logger.debug('GET method executed successfully')
	
	return render_template('main.html')
	
@app.route('/air_index.html')
def result():
	if 'state' in session:
		state = session['state']
		location = geofinder.geocode(state)
	
		longitude = location.longitude
		latitude = location.latitude 
		
			
		conn = http.client.HTTPSConnection("rapidweather.p.rapidapi.com")

		headers = {
			'X-RapidAPI-Key': "kindly-fetch-your-key-for-rapidweather-api",
			'X-RapidAPI-Host': "rapidweather.p.rapidapi.com"
			}

		conn.request("GET", "/data/2.5/air_pollution?lat="+ latitude + "&lon=" + longitude + "", headers=headers)

		res = conn.getresponse()
		data = res.read()


		all = data.decode("utf-8")
		pollution_index = json.loads(all)
		print(pollution_index)
		#print(all)
		print(pollution_index['list'][0]['main']['aqi']) 
		
		result = pollution_index['list'][0]['main']['aqi']
		
		if result <= 3:
			msg = 'Ideal: The Air Pollution Index is low at your location'
		elif 3 < result <= 6:
			msg = 'Warning:The Air Pollution is Moderate at your loction'
		elif 6 < result <=10:
			msg = 'At Risk: The Air Pollution Index is very high, take precaution'
		else:
			msg = 'Emergency: The Air Pollution Index is extreme today. Report status to appropriate local authorities '
			#print()
	
		#session.pop('state', None)
		return render_template('air_index.html', msg = msg)
	else:
		return render_template('404.html'), 404
	


if __name__ == "__main__": 
	app.run(debug=True)
