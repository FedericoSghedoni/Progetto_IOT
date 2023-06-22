from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883

direction = None


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("AlternativeDirection MQTT Client connected")
	else:
		print("MQTT Connection Error", rc)


def direction_alt(zones):
	# start MQTT client
	client = mqtt_client.Client("wind_alt")
	client.on_connect = on_connect
	client.connect(broker, port)
	client.loop_start()

	# init direction
	global direction
	value = input("Please enter a integer between 0 and 359:\n")
	value = int(value)
	for zone in zones:
		direction = value
		for turbine in zones[zone]["turbines"]:
			client.publish(f"{zone}/{turbine}/direction", str(value).zfill(3))
			print("published alt dir")

	# infinite loop
	while True:
		value = input("Please enter a integer between 0 and 359:\n")
		value = int(value)
		if abs(direction - value) > 5:
			for zone in zones:
				for turbine in zones[zone]["turbines"]:
					client.publish(f"{zone}/{turbine}/direction", str(value).zfill(3))
					print("published alt dir")


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

	direction_alt(zt_dic)
