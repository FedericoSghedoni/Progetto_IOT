"""
The Direction Thread uses meteo information to change the direction of the turbines.
The wind direction is downloaded every 10 minutes and it is sent to the turbines (via MQTT)
only if the difference with the current direction is higher than a threshold.
"""
from threading import *
import schedule
import requests
from paho.mqtt import client as mqtt_client

url = "https://api.weatherapi.com/v1/current.json?key=00590921f850414bb73194114232303&q="

broker = 'localhost'
port = 1883


def on_connection(client, userdata, flags, rc):
	if rc == 0:
		print("DirectionThread MQTT Client connected")
	else:
		print("MQTT Connection Error", rc)


class DirectionThread(Thread):
	def __init__(self, data, fake_dir = None):
		super(DirectionThread, self).__init__()
		self.data = data
		self.zones = [zone for zone in self.data]
		self.directions = {}
		self.client = mqtt_client.Client("wind_thread")
		self.client.on_connect = on_connection
		self.client.connect(broker, port)
		self.client.loop_start()
		self.fake_dir = fake_dir

		# Initialization of direction values
		for zone in self.data:
			complete_url = url + str(self.data[zone]["coords"][0]) + "," + str(self.data[zone]["coords"][1])
			meteo_json = requests.get(complete_url).json()
			direction = int(meteo_json["current"]["wind_degree"])  # deg
			if fake_dir is not None:
				direction = fake_dir
			self.directions[zone] = direction

			for turbine in self.data[zone]["turbines"]:
				self.client.publish(f"{zone}/{turbine}/direction", str(self.directions[zone]).zfill(3))
				#print(f"Published direction {direction} on turbine {zone}/{turbine}")

		schedule.every(10).minutes.do(self.update)

	def run(self):
		while True:
			schedule.run_pending()

	def update(self):
		for zone in self.zones:
			complete_url = url + str(self.data[zone]["coords"][0]) + "," + str(self.data[zone]["coords"][1])
			meteo_json = requests.get(complete_url).json()
			direction = int(meteo_json["current"]["wind_degree"])  # deg

			if self.fake_dir is not None:
				direction = self.fake_dir

			if 5 < abs(self.directions[zone] - direction) < 355:
				print(f"Change direction of zone {zone} from {self.directions[zone]} to {direction}")
				self.directions[zone] = direction
				direction = str(direction).zfill(3)

				for turbine in self.data[zone]["turbines"]:
					self.client.publish(f"{zone}/{turbine}/direction", direction)
					#print(f"Published direction {direction} on turbine {zone}/{turbine}")


if __name__ == "__main__":
	zt_dic = {
		"01": {
			"coords": (44.5, 10.9),
			"turbines": ["001", "002"],
		},
		"02": {
			"coords": (44.5, 10.9),
			"turbines": ["003"],
		}
	}
	direction_t = DirectionThread(zt_dic)
	direction_t.start()
