from threading import *
import schedule
import requests
from paho.mqtt import client as mqtt_client

api_key = "e583a33a1ffef78a771ec70327961706"
url = "https://api.openweathermap.org/data/2.5/weather?"

broker = 'localhost'
#broker = "localhost"
port = 1883


def check_connection(client, userdata, flags, rc):
	if rc == 0:
		print("MQTT Client connected")
	else:
		print("MQTT Connection Error", rc)


class OrientationThread(Thread):
	def __init__(self, zones):
		super(OrientationThread, self).__init__()
		self.zones = zones
		self.direction = {}
		self.client = mqtt_client.Client("wind_thread")
		self.client.on_connect = check_connection

		# initialize direction values
		for zone_name in self.zones:
			print("init")
			complete_url = url + "lat=" + str(self.zones[zone_name][0]) + "&lon=" + str(self.zones[zone_name][1]) + "&appid=" + api_key
			meteo_json = requests.get(complete_url).json()
			direction = float(meteo_json["wind"]["deg"])  # deg
			self.direction[zone_name] = direction

			self.client.connect(broker, port)
			self.client.publish(f"{zone_name}/direction", self.direction[zone_name])

		schedule.every(1).minutes.do(self.update)

	def run(self):
		while True:
			schedule.run_pending()
			#time.sleep(30)

	def update(self):
		print("update function")
		for zone_name in self.zones:
			complete_url = url + "lat=" + str(self.zones[zone_name][0]) + "&lon=" + str(self.zones[zone_name][1]) + "&appid=" + api_key
			meteo_json = requests.get(complete_url).json()
			direction = float(meteo_json["wind"]["deg"])  # deg

			if abs(self.direction[zone_name] - direction) > 10:
				print(f"Change direction of zone {zone_name} from {self.direction[zone_name]} to {direction}")
				self.direction[zone_name] = direction

				self.client.connect(broker, port)
				self.client.publish(f"{zone_name}/direction", self.direction[zone_name])


if __name__ == "__main__":
	zone_dic = {
		"01": (44.5, 10.9)
	}
	wind_t = OrientationThread(zone_dic)
	wind_t.start()
