from threading import *
import schedule
import requests
from paho.mqtt import client as mqtt_client

url = "http://api.weatherapi.com/v1/current.json?key=00590921f850414bb73194114232303&q="

broker = 'localhost'
port = 1883


def check_connection(client, userdata, flags, rc):
	if rc == 0:
		print("DirectionThread MQTT Client connected")
	else:
		print("MQTT Connection Error", rc)


class DirectionThread(Thread):
	def __init__(self, zones, zone_turbine):
		super(DirectionThread, self).__init__()
		self.zones = zones
		self.zone_turbine = zone_turbine
		self.direction = {}
		self.client = mqtt_client.Client("wind_thread")
		self.client.on_connect = check_connection
		self.client.connect(broker, port)
		self.client.loop_start()

		# initialize direction values
		for zone_name in self.zones:
			complete_url = url + str(self.zones[zone_name][0]) + "," + str(self.zones[zone_name][1])
			meteo_json = requests.get(complete_url).json()
			direction = int(meteo_json["current"]["wind_degree"])  # deg
			self.direction[zone_name] = direction

			for turb in self.zone_turbine[zone_name]:
				self.client.publish(f"{zone_name}/{turb}/direction", str(self.direction[zone_name]).zfill(3))
				print(f"Pubblicata {zone_name}/{turb}/direction")

		schedule.every(10).minutes.do(self.update)

	def run(self):
		while True:
			schedule.run_pending()

	def update(self):
		for zone_name in self.zones:
			complete_url = url + str(self.zones[zone_name][0]) + "," + str(self.zones[zone_name][1])
			meteo_json = requests.get(complete_url).json()
			direction = int(meteo_json["current"]["wind_degree"])  # deg

			if 5 < abs(self.direction[zone_name] - direction) < 355:
				print(f"Change direction of zone {zone_name} from {self.direction[zone_name]} to {direction}")
				self.direction[zone_name] = direction
				direction = str(direction).zfill(3)

				#self.client.connect(broker, port)
				for turb in self.zone_turbine[zone_name]:
					self.client.publish(f"{zone_name}/{turb}/direction", direction)
					print(f"Pubblicata {zone_name}/{turb}/direction")


if __name__ == "__main__":
	zone_dic = {
		"01": (44.5, 10.9)
	}
	wind_t = DirectionThread(zone_dic)
	wind_t.start()
