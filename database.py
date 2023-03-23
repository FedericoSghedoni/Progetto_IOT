import sqlite3


def create_tables():
	connection = sqlite3.connect("database.db")

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


def insert_arduino(zone, idpala, date, hour, dic):
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	stringa = f"""INSERT INTO arduino 
				VALUES ('{zone}', '{idpala}', '{date}', '{hour}', '{dic["speed"]}', '{dic["power"]}', '{dic["current"]}', '{dic["error"]}' )"""
	cursor.execute(stringa)

	# rendo permanenti gli INSERT
	connection.commit()


def insert_meteo(x):
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	stringa = f"REPLACE INTO meteo VALUES ('{x[0]}', '{x[1]}', {x[2]}, '{x[3]}', '{x[4]}', '{x[5]}', '{x[6]}', '{x[7]}')"
	cursor.execute(stringa)

	# rendo permanenti gli INSERT
	connection.commit()


def get_turbin_info(idpala):
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()
	command = f"""SELECT * FROM arduino
	WHERE id='{idpala}'
	"""
	result = cursor.execute(command)
	return result.fetchall()


def get_recent_meteo(n=47):
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()
	result = cursor.execute(f"""SELECT date, hour, temperature, speed, direction, pressure
	FROM meteo ORDER BY date DESC, hour DESC LIMIT {n}""")
	return result.fetchall()


if __name__ == '__main__':
	# Run create_tables only if the db doesn't already exist
	create_tables()

	dic = {
		"current": 200,
		"power": 200,
		"error": "no error",
		"speed": 100
	}
	# Insert the dic values inside arduino table
	#insert_arduino("01", "001", "2023-03-01", "17:50:00", dic)

	# Return info for the specified turbine
	#get_turbin_info("001")

	m1 = ["2023-03-17", "12:00:00", 11.1, 3.05, 74, 1.0086, None, "overcast clouds"]
	# Insert the m values inside meteo table
	#insert_meteo(m1)

	#rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
	#print(rows)
