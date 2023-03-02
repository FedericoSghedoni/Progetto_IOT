import sqlite3


def checkTableExists(dbcon, tablename):
	dbcur = dbcon.cursor()
	dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
	if dbcur.fetchone()[0] == 1:
		dbcur.close()
		return True
	dbcur.close()
	return False


def initialize_db():
	connection = sqlite3.connect("database.db")

	if not checkTableExists(connection, "arduino"):
		cursor = connection.cursor()
		cursor.execute("""CREATE TABLE arduino (
				   zone TEXT,
				   id TEXT,
				   date DATE,
				   hour TIME,
				   current FLOAT,
				   power FLOAT,
				   speed FLOAT,
				   error TEXT,
				   voltage FLOAT)""")

	if not checkTableExists(connection, "meteo"):
		cursor = connection.cursor()
		cursor.execute("CREATE TABLE meteo (" +
				   "date DATE, " +
				   "hour TIME, " +
				   "weather TEXT, " +
				   "temperature FLOAT, " +
				   "humidity FLOAT, " +
				   "wind_speed FLOAT, " +
				   "wind_dir TEXT)")


def insert_arduino(idpala, dic, date, hour):
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	stringa = f"""INSERT INTO arduino 
	VALUES ('{idpala}', '{date}', '{hour}', '{dic["current"]}', '{dic["power"]}', '{dic["speed"]}', '{dic["direction"]}', '{dic["error"]}', '{dic["temperature"]}' )"""
	cursor.execute(stringa)
	#cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")

	# rendo permanenti gli INSERT
	connection.commit()


def insert_meteo(date, hour, weather, temperature, humidity, speed, direction):
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	stringa = f"INSERT INTO meteo VALUES ('{date}', '{hour}', '{weather}', '{temperature}', '{humidity}', '{speed}', '{direction}')"
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


if __name__ == '__main__':
	#initialize_db()
	dic = {
		"current": 200,
		"power": 200,
		"temperature": 23.6,
		"error": "no error",
		"speed": 100,
		"direction": "nord"
	}
	insert_arduino("001", dic, "2023-03-01", "17:50:00")
	#get_turbin_info("001")

	#rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
	#print(rows)
