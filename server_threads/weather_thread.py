"""
The Weather Thread downloads meteo information from the internet. At each hour it downloads the meteo of the following
day at the same hour, composed by datetime, temperature, pressure, wind direction, wind velocity, weather condition.
These data are saved in the database table 'meteo'. These data are also used to predict the produced power (also this
value is inserted in 'meteo').
"""

from threading import *
import time
import schedule
import requests
import torch

from lstm_model import predict
from database import insert_meteo, get_recent_meteo
import numpy as np

url = "https://api.weatherapi.com/v1/forecast.json?key=00590921f850414bb73194114232303&q=44.64,10.92&days=2&aqi=no&alerts=no"


# Download one meteo information for each hour of today and tomorrow
# and insert them in the database table 'meteo'
def download_all():
	meteo_json = requests.get(url).json()
	for day_meteo in meteo_json["forecast"]["forecastday"]:
		for hour_meteo in day_meteo["hour"]:
			dt = hour_meteo["time"]
			temperature = float(hour_meteo["temp_c"])
			pressure = float(hour_meteo["pressure_mb"]) * 0.0009869  # convert from millibar to atm
			direction = float(hour_meteo["wind_degree"])
			speed = float(hour_meteo["wind_mph"]) * 0.44704  # convert mph to m/s
			description = hour_meteo["condition"]["text"]

			insert_meteo(
				[dt.split(' ')[0], dt.split(' ')[1] + ":00", temperature, speed, direction, pressure, 0, description])
	print("All meteo download completed")


# Download the meteo information for tomorrow at this hour and insert it in
# the database table 'meteo'. Inserts in the database also the power prediction.
def download(checkpoint):
	meteo_json = requests.get(url).json()
	current_hour = int(meteo_json["location"]["localtime"].split(' ')[1].split(':')[0])

	future_meteo = meteo_json["forecast"]["forecastday"][1]["hour"][current_hour]
	temperature = float(future_meteo["temp_c"])
	pressure = float(future_meteo["pressure_mb"]) * 0.0009869  # convert to atm
	speed = float(future_meteo["wind_mph"]) * 0.44704  # m/s
	direction = int(future_meteo["wind_degree"])  # deg
	dt = future_meteo["time"]
	month = int(dt.split('-')[1])
	day = int(dt.split('-')[2].split(' ')[0])
	description = future_meteo["condition"]["text"]

	# Create the vector to be inserted in database
	db_in = [dt.split(' ')[0], dt.split(' ')[1] + ":00", temperature, speed, direction, pressure]

	# Create the input for lstm model
	lstm_in = np.array([month, day, current_hour, temperature, speed, direction, pressure])
	met = get_recent_meteo()
	for i in met:
		i = list(i)
		d = i.pop(0)
		h = i.pop(0)
		i.insert(0, int(h.split(':')[0]))  # ora
		i.insert(0, int(d.split('-')[2]))  # giorno
		i.insert(0, int(d.split('-')[1]))  # mese
		lstm_in = np.append(lstm_in, i)

	# Predict power value
	lstm_in = lstm_in.reshape(-1, 7)
	lstm_in = np.flip(lstm_in, axis=0)
	power = predict(lstm_in, checkpoint)

	# Complete database values and insert them
	db_in.append(power[0][0])
	db_in.append(description)
	insert_meteo(db_in)
	print("Meteo download completed")


def calc_new_delay(delay: int) -> int:
	"""Calc the dalay of timer based on what time is it"""
	seconds_today = (time.localtime().tm_hour * 3600) + (time.localtime().tm_min * 60) + time.localtime().tm_sec
	passed_from_last = seconds_today % delay
	new_delay = delay - passed_from_last
	return new_delay


# Weather Thread implemetation: run function download one time each hour
class WeatherThread(Thread):
	def __init__(self, checkpoint):
		super(WeatherThread, self).__init__()
		self.download = download
		self.checkpoint = checkpoint

	def run(self):
		while True:
			time.sleep(calc_new_delay(3600))
			self.download(self.checkpoint)


if __name__ == "__main__":
	download_all()
	#download()
	#weather_t = WeatherThread()
	#weather_t.start()
	#weather_t.join()
