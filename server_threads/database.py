import sqlite3
import os


def create_tables():
	path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
	connection = sqlite3.connect(os.path.join(path, "Winduino_WebAPP", "database.db"))

	cursor = connection.cursor()
	cursor.execute("""CREATE TABLE arduino (
				   zone TEXT,
				   id TEXT,
				   date DATE,
				   hour TIME,
				   speed FLOAT,
				   power FLOAT,
				   current FLOAT,
				   error TEXT)""")

	cursor.execute("""CREATE TABLE meteo (
						date DATE NOT NULL,
						hour TIME NOT NULL,
						temperature FLOAT,
						speed FLOAT,
						direction FLOAT,
						pressure FLOAT,
						power FLOAT,
						description TEXT,
						PRIMARY KEY (date, hour))""")


# Insert a new row in the 'arduino' table
def insert_arduino(zone, idpala, date, hour, d):
	path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
	connection = sqlite3.connect(os.path.join(path, "Winduino_WebAPP", "database.db"))

	with connection:
		cursor = connection.cursor()

		stringa = f"""INSERT INTO arduino 
					VALUES ('{zone}', '{idpala}', '{date}', '{hour}', {d["R_value_"]}, {d["mW_value_"]}, {d["mA_value_"]}, '{d["Error"]}' )"""
		cursor.execute(stringa)


# Insert a row in the 'meteo' table. The rows are have primary key date-time
# so if the key is already present the row will be replaced.
def insert_meteo(x):
	path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
	connection = sqlite3.connect(os.path.join(path, "Winduino_WebAPP", "database.db"))

	with connection:
		cursor = connection.cursor()

		stringa = f"REPLACE INTO meteo VALUES ('{x[0]}', '{x[1]}', {x[2]}, {x[3]}, {x[4]}, {x[5]}, {x[6]}, '{x[7]}')"
		cursor.execute(stringa)


# Return the 47 most recent entries of the 'meteo'. It's called by the Weather Thread when it does
# the power prediction with the LSTM model.
def get_recent_meteo(n=47):
	path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
	#path = r"C:\Users\Serena\Documents\Università\4°-5° anno (21-22, 22-23)\IOT and 3D intelligent systems\IOT_project\Progetto_IOT"
	connection = sqlite3.connect(os.path.join(path, "Winduino_WebAPP", "database.db"))

	with connection:
		cursor = connection.cursor()
		result = cursor.execute(f"""SELECT date, hour, temperature, speed, direction, pressure
		FROM meteo ORDER BY date DESC, hour DESC LIMIT {n}""")
		return result.fetchall()


# Modify the power value of one entry of the 'meteo' table. The entry is identified
# by date and time. The old power value was the prediction, the new power value is
# the real power generated.
def update_power(new_val, date, hour):
	path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
	connection = sqlite3.connect(os.path.join(path, "Winduino_WebAPP", "database.db"))

	with connection:
		cursor = connection.cursor()
		cursor.execute(f"UPDATE meteo SET power={new_val} WHERE date='{date}' AND hour='{hour}'")


if __name__ == '__main__':
	# Run create_tables only if the db doesn't already exist
	#create_tables()

	import random
	zones = ["01", "02", "03"]
	turbs = ["001", "002", "003"]
	hours = ["00","01", "02","03", "04", "05", "06", "07", "08"]
	mins = ["00", "10", "20", "30", "40", "50"]
	for zone in zones:
		for turb in turbs:
			for hour in hours:
				for mi in mins:
					d = {"mA_value_": round(random.uniform(30.00, 50.00), 2),
						 "mW_value_": round(random.uniform(500.00, 2500.00), 2),
						 "Error": "OK",
						 "R_value_": round(random.uniform(15.00, 32.00), 2)}
					insert_arduino(zone, turb, "2023-06-30", hour+":"+mi+":00", d)
	# Insert the dic values inside arduino table
	#insert_arduino("01", "001", "2023-03-01", "17:50:00", dic)

	# Return info for the specified turbine
	#get_turbin_info("001")

	m1 = ["2023-03-17", "12:00:00", 11.1, 3.05, 74, 1.0086, None, "overcast clouds"]
	# Insert the m values inside meteo table
	#insert_meteo(m1)
	#update_power(11.0, "2023-03-23", "12:00")
