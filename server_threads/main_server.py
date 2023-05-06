from weather_thread import WeatherThread
from direction_thread import DirectionThread
from arduino_thread import ArduinoThread


if __name__ == '__main__':
    # start weather thread (download weather periodially and predicts power generation)
    weather_t = WeatherThread()
    weather_t.start()

    # start direction thread (modify turbines direction accordingly with the wind)
    zone_coords = {
        "01": (44.5, 10.9)
    }
    zone_turbine = {
        "01": ["001", "002"],
        "02": ["003"]
    }
    orientation_t = DirectionThread(zone_coords, zone_turbine)
    orientation_t.start()

    # start arduino thread (receive turbines info)

    arduino_t = ArduinoThread(zone_turbine)
    arduino_t.start()
