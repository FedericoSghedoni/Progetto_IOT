import sqlite3


def initialize_db():
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	cursor.execute("CREATE TABLE arduino (" +
				   "id TEXT, " +
				   "date DATE, " +
				   "hour TIME, " +
				   "current INTEGER, " +
				   "power INTEGER, " +
				   "speed FLOAT, " +
				   "direction TEXT, " +
				   "error TEXT, " +
				   "temperature FLOAT)")

	cursor.execute("CREATE TABLE meteo (" +
				   "date DATE, " +
				   "hour TIME, " +
				   "weather TEXT, " +
				   "temperature FLOAT, " +
				   "humidity FLOAT, " +
				   "wind_speed FLOAT, " +
				   "wind_dir TEXT)")


def insert_arduino(idpala, date, hour, current, power, speed, direction, error, temperature):
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	stringa = f"INSERT INTO arduino VALUES ('{idpala}', '{date}', '{hour}', '{current}', '{power}', '{speed}', '{direction}', '{error}', '{temperature}' )"
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


if __name__ == '__main__':
	#initialize_db()
	insert_arduino("001", "2023/02/25", "17:53:00", 100.0, 200.0, 10, "nord", "no error", 20.5)

	#rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
	#print(rows)


