import unittest
import requests

# url = "http://10.43.33.230:8000/broker/temperature"
# url = "http://localhost:8000/broker/temperature"
# url = "https://localhost:443/broker/temperature"
url = "http://35.230.39.10/broker/temperature"
validId = 1
invalidId = 6
validTimestamp = 1516740562
validTemperature = 27.7
invalidTemperature = -200


def suma(a, b):
    return a+b


def send_to_database(id, timestamp, temperature):
    data = {
        "id": id,
        "timestamp": validTimestamp,
        "temperature": temperature,
    }
    resp = requests.post(url, json=data)
    return resp.text


class LearningCase(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(suma(2, 3), 5)

    def test_correct_values(self):
        self.assertEqual(send_to_database(validId, validTimestamp, validTemperature), "OK.\n")

    def test_invalid_id(self):
        self.assertEqual(send_to_database(invalidId, validTimestamp, validTemperature), "Invalid ID.\n")

    def test_invalid_temperature(self):
        self.assertEqual(send_to_database(validId, validTimestamp, invalidTemperature), "Invalid temperature.\n")


def main():
    unittest.main()


if __name__ == "__main__":
    main()






# print(" URL:\t\t%s" % resp.url)
# print(" encoding:\t%s" % resp.encoding)
# print(" status_code:\t%s" % resp.status_code)
# print(" text:\t\t%s" % resp.text)
