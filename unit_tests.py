import unittest
import requests
import calendar
import time

url = "https://35.230.39.10:443/broker/status"
validId = 1
invalidId = 6
validTemperature = 27
invalidTemperatureUnder = -129
invalidTemperatureOver = 128
validHumidity = 16
invalidHumidityUnder = -1
invalidHumidityOver = 101
validLight = 120
invalidLightUnder = -1
invalidLightOver = 151


def send_to_database(id, temperature, humidity, light):
    data = {
        "id": id,
        "timestamp": calendar.timegm(time.gmtime()),
        "temperature": temperature,
        "humidity": humidity,
        "light": light,
    }
    resp = requests.post(url, json=data, verify=False)
    return resp.text


class LearningCase(unittest.TestCase):
    def test_valid_status(self):
        self.assertEqual(send_to_database(validId, validTemperature, validHumidity, validLight), "OK.\n")

    def test_invalid_id(self):
        self.assertEqual(send_to_database(invalidId, validTemperature, validHumidity, validLight), "Invalid ID.\n")

    def test_invalid_temperature_under(self):
        self.assertEqual(send_to_database(validId, invalidTemperatureUnder, validHumidity, validLight), "Invalid data.\n")

    def test_invalid_temperature_over(self):
        self.assertEqual(send_to_database(validId, invalidTemperatureOver, validHumidity, validLight), "Invalid data.\n")

    def test_invalid_humidity_under(self):
        self.assertEqual(send_to_database(validId, validTemperature, invalidHumidityUnder, validLight), "Invalid body.\n")

    def test_invalid_humidity_over(self):
        self.assertEqual(send_to_database(validId, validTemperature, invalidHumidityOver, validLight), "Invalid data.\n")

    def test_invalid_light_under(self):
        self.assertEqual(send_to_database(validId, validTemperature, validHumidity, invalidLightUnder), "Invalid body.\n")

    def test_invalid_light_over(self):
        self.assertEqual(send_to_database(validId, validTemperature, validHumidity, invalidLightOver), "Invalid data.\n")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
