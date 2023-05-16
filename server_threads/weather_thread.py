"""
Weather Thread download meteo informations every 3 hour, uses these informations
to predict the produced enery and saves the values in the database.
"""
from threading import *
import time
import schedule
import requests
from lstm_model import predict
from database import insert_meteo, get_recent_meteo
import numpy as np

url = "http://api.weatherapi.com/v1/forecast.json?key=00590921f850414bb73194114232303&q=44.64,10.92&days=2&aqi=no&alerts=no"


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

			insert_meteo([dt.split(' ')[0], dt.split(' ')[1] + ":00", temperature, speed, direction, pressure, 0, description])


def download():
	print("Download")
	meteo_json = requests.get(url).json()
	current_hour = int(meteo_json["location"]["localtime"].split(' ')[1].split(':')[0])

	future_meteo = meteo_json["forecast"]["forecastday"][1]["hour"][current_hour]
	temperature = float(future_meteo["temp_c"])
	pressure = float(future_meteo["pressure_mb"]) * 0.0009869  # convert to atm
	speed = float(future_meteo["wind_mph"]) * 0.44704  # m/s
	direction = float(future_meteo["wind_degree"])  # deg
	dt = future_meteo["time"]
	month = int(dt.split('-')[1])
	day = int(dt.split('-')[2].split(' ')[0])
	description = future_meteo["condition"]["text"]

	db_in = [dt.split(' ')[0], dt.split(' ')[1] + ":00", temperature, speed, direction, pressure]

	# collect the inputs for lstm model
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

	# predict power value
	lstm_in = lstm_in.reshape(-1, 7)
	power = predict(lstm_in)

	# complete database values and insert them
	db_in.append(power[0][0])
	db_in.append(description)
	insert_meteo(db_in)
	print("finish download")


class WeatherThread(Thread):
	def __init__(self):
		super(WeatherThread, self).__init__()
		self.download = download

		schedule.every().hour.at(":18").do(self.download)

	def run(self):
		while True:
			schedule.run_pending()
			time.sleep(1)


if __name__ == "__main__":
	download_all()
	#download()
	#weather_t = WeatherThread()
	#weather_t.start()
	#weather_t.join()
