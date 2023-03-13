from threading import *
import time
import schedule
import requests
from lstm_model import predict
from database import insert_meteo

api_key = "e583a33a1ffef78a771ec70327961706"
url = "https://api.openweathermap.org/data/2.5/forecast?lat=10.9&lon=44.5&appid=" + api_key


def download():
	#print("func")
	response = requests.get(url)
	data = response.json()
	x = data["list"]
	temperature = x[7]["main"]["temp"]
	pressure = x[7]["main"]["pressure"]
	speed = x[7]["wind"]["speed"]
	direction = x[7]["wind"]["deg"]
	month = int(x[7]["dt_txt"].split('-')[1])
	day = int(x[7]["dt_txt"].split('-')[2].split(' ')[0])
	h = int(x[7]["dt_txt"].split(' ')[1].split(':')[0])
	description = x[7]["weather"][0]["description"]

	x = [month, day, h, temperature, speed, direction, pressure]
	power = predict(x)
	x.append(description)
	x.append(power)
	insert_meteo(x)


class WeatherThread(Thread):
	def __init__(self):
		super(WeatherThread, self).__init__()
		self.download = download

		times = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
		for t in times:
			schedule.every().day.at(t).do(self.download)

	def run(self):
		while True:
			schedule.run_pending()
			time.sleep(60)



if __name__ == "__main__":
	weather_t = WeatherThread()
	weather_t.start()
