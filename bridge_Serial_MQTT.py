import serial
import serial.tools.list_ports
import paho.mqtt.client as mqtt
import time

class Bridge():

	def __init__(self, port):
		self.buffer = []
		self.datiZona = {}
		self.sogliaMax = 35
		self.sogliaMin = 10
		self.currentState = 0
		self.ser = None
		self.port = port
		self.setupSerial(port)
		self.setupMQTT()
		self.timer = 0

	def setupSerial(self, port):        
		try:
			# apre la porta seriale
			self.ser = serial.Serial(port.device, 9600, timeout=2)
			time.sleep(2)
			# scrive un messaggio sull'self
			self.ser.write(b'\xff')
			# legge la risposta dell'self
			response = self.ser.read()
			# verifica se l'self ha risposto correttamente
			if response == b'\xfe':
				print(f"Arduino connesso alla porta {port.device}")
				# se l'self è stato trovato aggiungi il suo id al dizionario con il buffer associato, esci dal ciclo
				size_zona = int(self.ser.read().decode())
				self.zona = self.ser.read(size_zona).decode()
				#size_id = int(self.ser.read().decode())
				self.id = self.ser.read(3).decode()
				print(self.zona, self.id)
				self.portName = port.device
				return True
			else:
				error = self.ser.read(27)
				print(error)
				# se self non ha risposto correttamente, chiude la porta seriale
				self.ser.close()
				print('Errore nella connessione')
				return False
		except (OSError, serial.SerialException):
			pass

	def setupMQTT(self):
		self.clientMQTT = mqtt.Client("Bridge" + self.zona + "_" + self.id)
		self.clientMQTT.on_connect = self.on_connect
		self.clientMQTT.on_message = self.on_message
		self.clientMQTT.on_log = self.on_log
		broker = 'localhost'
		port = 1883
		self.clientMQTT.connect(broker, port)
		self.clientMQTT.loop_start()

	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			print("Bridge Connected to MQTT Broker!")
		else:
			print("Failed to connect, return code %d\n", rc)

		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		self.clientMQTT.subscribe(self.zona + '/' + self.id + '/' + "direction")
		self.clientMQTT.subscribe(self.zona + '/+/R_value_')
		self.clientMQTT.subscribe(self.zona + '/+/Error')

	# The callback for when a PUBLISH message is received from the server.
	def on_message(self, client, userdata, msg):
		print("Received " + msg.topic + " " + str(msg.payload))  # stampa DEBUG
		if msg.topic == self.zona + '/' + self.id + '/' + "R_value_":
			dati = list(self.datiZona.values())
			if len(dati) != 0:
				media = sum(dati) / len(dati)
				futureState = None
				value = float(msg.payload.decode())
				if self.currentState == 0:
					if value > self.sogliaMax:
						futureState = 1
						self.ser.write(b'L0')  # Spegni Led Malfunzionamento
						self.clientMQTT.publish(self.zona + '/' + self.id + '/' + "Error", 0)
					elif value < media-15 or value < 0:  # controllo errori
						futureState = 2
					else:
						self.ser.write(b'L0')  # Spegni Led Malfunzionamento
						self.clientMQTT.publish(self.zona + '/' + self.id + '/' + "Error", 0)
     
				elif self.currentState == 1:  # check velocità > media
					if value > media+10:
						self.ser.write(b'A1')  # Ruota
						self.timer = time.time()
						futureState = 4
					else: futureState = 3

				elif self.currentState == 2:  # stato intermedio, 2° check errori
					if value < media-15 or value < 0:
						self.ser.write(b'L1')  # Accendi Led Malfunzionamento
						self.clientMQTT.publish(self.zona + '/' + self.id + '/' + "Error", 1)
					futureState = 0

				elif self.currentState == 3:  # stato intermedio, 2° check > soglia
					if value > self.sogliaMax:
						self.ser.write(b'A1')  # Ruota
						self.timer = time.time()
						futureState = 4
					else: futureState = 0

				elif self.currentState == 4:
					if (time.time() - self.timer)/1000 >= 3000:
						self.ser.write(b'A0')  # Ruota Pale verso vento
						futureState = 0

				self.currentState = futureState

		elif msg.topic == self.zona + '/' + self.id + '/' + "direction":
			print("ciao")
			self.ser.write(b'D')  # Ruota Pale verso vento
			self.ser.write(msg.payload)
			print(self.ser.readString())

		elif 'R_value_' in msg.topic:
			value = msg.payload.decode()
			zona, id, name = msg.topic.split('/')
			if self.id != id:
				self.datiZona[id] = int(value)
		elif 'Error' in msg.topic:
			if self.id != id:
				self.datiZona.pop(id)

	def on_log(self, client, userdata, level, buf):
		print("log: ", buf)

	def readData(self):
		#look for a byte from serial
		while self.ser.in_waiting > 0:
			# data available from the serial port
			lastchar = self.ser.read(1)
			if lastchar == b'\xfe':  # EOL
				print("\nValue received")
				self.useData()
				self.buffer = []
			else:
				# append
				self.buffer.append(lastchar)

	def useData(self):
		print(self.buffer.decode()) #stampa DEBUG
		# I have received a packet from the serial port. I can use it

		if self.buffer[0] != b'\xff':
			print('Pacchetto errato')
			return False
		numval = int(self.buffer[1].decode()) # legge size del pacchetto
		val = ''
		for i in range (numval):
			if numval - i == 2:
				val = val + '.'
			val = val + self.buffer[i+2].decode() # legge valore del pacchetto
		#print(val)
		sensor_name = ''
		SoN = numval + 2
		sensorLen = len(self.buffer) - (SoN)
		for j in range (sensorLen):
			sensor_name = sensor_name + str(self.buffer[j + SoN].decode())
		res, mid = self.clientMQTT.publish(self.zona + '/' + self.id + '/' + sensor_name, val)

