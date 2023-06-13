from weather_thread import WeatherThread
from direction_thread import DirectionThread
from arduino_thread import ArduinoThread


if __name__ == '__main__':
    # start Weather Thread
    weather_t = WeatherThread()
    weather_t.start()

    zt_dic = {
        "01" : {
            "coords" : (44.5, 10.9),
            "turbines" : ["001", "002"],
        },
        "02" : {
            "coords" : (44.5, 10.9),
            "turbines": ["003"],
        }
    }
    zone_turbine = {
        "01": ["001", "002"],
        "02": ["003"]
    }

    # start Direction Thread (modify turbines direction accordingly with the wind)
    # inserire fake_dir = True per usare direzioni fittizie
    direction_t = DirectionThread(zt_dic)
    direction_t.start()

    # start arduino thread (receive turbines info)
    arduino_t = ArduinoThread(zone_turbine)
    arduino_t.start()

    weather_t.join()
    direction_t.join()
    arduino_t.join()
