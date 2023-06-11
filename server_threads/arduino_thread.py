"""
Python thread that handles the messages coming from the arduino boards. It saves the information
in the database table 'arduino' and also handle the calculation of the effective generated power.
"""
from threading import *
from paho.mqtt import client as mqtt_client
import schedule
from database import insert_arduino, update_power
from datetime import datetime, date

broker = 'localhost'
port = 1883

turbine_register = {}
# teniamo un conteggio di power unico per tutto il parco eolico
power_register = 0


def on_connect(client, userdata, flags, rc):
	# Dice cosa fare quando si connette al broker
	if rc == 0:
		print("ArduinoThread Connected to MQTT Broker!")
	else:
		print("Failed to connect, return code %d\n", rc)


def update():
	global power_register
	update_power(power_register / (60 / 10), date.today(), str(datetime.now().hour) + ":00:00")
	power_register = 0


def on_message(client, userdata, msg):
	global power_register, turbine_register
	# Dice cosa fare quando arriva un nuovo messaggio
	print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
	topic = msg.topic.split("/")
	key = topic[0] + "/" + topic[1]

	if topic[2] == 'mW_value_':
		power_register += (float(msg.payload.decode()) * 100)
		turbine_register[key][topic[2]] = float(msg.payload.decode()) * 100
	elif topic[2] == 'Error':
		if int(msg.payload.decode()) == 1:
			turbine_register[key][topic[2]] = 'Error'
		else:
			turbine_register[key][topic[2]] = 'OK'
	elif topic[2] == 'R_value_':
		turbine_register[key][topic[2]] = float(msg.payload.decode()) / 10
	else:  # mA_value_
		turbine_register[key][topic[2]] = float(msg.payload.decode()) * 2


	turbine_register[key][topic[2]] = msg.payload.decode()
	if len(turbine_register[key]) == 4:
		insert_arduino(topic[0], topic[1], date.today(), datetime.now().strftime("%H:%M:%S"), turbine_register[key])
		turbine_register[key] = {}


class ArduinoThread(Thread):
	def __init__(self, zt_list):
		super(ArduinoThread, self).__init__()
		self.zt_list = zt_list
		self.client = mqtt_client.Client("arduino_thread")
		self.client.on_connect = on_connect
		self.client.on_message = on_message
		self.client.connect(broker, port)

		self.client.subscribe("+/+/mW_value_")
		self.client.subscribe("+/+/mA_value_")
		self.client.subscribe("+/+/R_value_")
		self.client.subscribe("+/+/Error")

		self.client.loop_start()

		schedule.every().hour.at(":00").do(update)

		# initialize register dictionary
		for z in zt_list:
			for t in zt_list[z]:
				turbine_register[z + "/" + t] = {}

	def run(self) -> None:
		while True:
			schedule.run_pending()


if __name__ == "__main__":
	zone_turbine = {
		"01": ["001", "002"],
		"02": ["003"]
	}
	#arduino_t = ArduinoThread(zone_turbine)
	#arduino_t.start()
	update()
