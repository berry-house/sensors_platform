import unittest
import requests
import calendar
import time

# url = "http://10.43.33.230:8000/broker/temperature"
# url = "http://localhost:8000/broker/temperature"
# url = "https://localhost:443/broker/temperature"
url = "http://35.230.39.10/broker/temperature"
validId = 1
invalidId = 6
validTemperature = 27.7
invalidTemperature = -200


def send_to_database(id, temperature):
    data = {
        "id": id,
        "timestamp": calendar.timegm(time.gmtime()),
        "temperature": temperature,
    }
    resp = requests.post(url, json=data)
    return resp.text


class LearningCase(unittest.TestCase):
    def test_correct_values(self):
        self.assertEqual(send_to_database(validId, validTemperature), "OK.\n")

    def test_invalid_id(self):
        self.assertEqual(send_to_database(invalidId, validTemperature), "Invalid ID.\n")

    def test_invalid_temperature(self):
        self.assertEqual(send_to_database(validId, invalidTemperature), "Invalid temperature.\n")


def main():
    unittest.main()


if __name__ == "__main__":
    main()






# print(" URL:\t\t%s" % resp.url)
# print(" encoding:\t%s" % resp.encoding)
# print(" status_code:\t%s" % resp.status_code)
# print(" text:\t\t%s" % resp.text)
