import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit

from Winduino_WebApp.apps.config import config_dict
from Winduino_WebApp.apps import create_app, db

from weather_thread import WeatherThread
from direction_thread import DirectionThread
from arduino_thread import ArduinoThread

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT = ' + app_config.ASSETS_ROOT)

if __name__ == "__main__":
    # START SERVER'S THREADS
    # start weather thread (download weather periodially and predicts power generation)
    weather_t = WeatherThread()
    weather_t.start()

    # start direction thread (modify turbines direction accordingly with the wind)
    zone_coords = {
        "01": (44.5, 10.9)
    }
    direction_t = DirectionThread(zone_coords)
    direction_t.start()

    # start arduino thread (receive turbines info)
    zone_turbine = {
        "01": ["001", "002"]
    }
    arduino_t = ArduinoThread(zone_turbine)
    arduino_t.start()
    
    app.run()
