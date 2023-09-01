from fastcom.test import SpeedTestGroup as Fast
from flask import Flask, jsonify

group = Fast(servers=1, iterations=1, trim=10)

app = Flask(__name__)

TIMEOUT = 30

def formating(median: str) -> float:
    """

    :param median: str the following form: XXX.XX Mbps
    :return speed: float of the median formatted
    """

    # check if it's a 3-digit, a 2-digit, or a one-digit number and convert it to a float
    number_in_digit = 0
    speed = 0.0
    if len(median) == 11:  # 3-digit number
        number_in_digit = median[:6]
        speed = float(number_in_digit[0]) * 100
        speed += float(number_in_digit[1]) * 10
        speed += float(number_in_digit[2])
        speed += float(number_in_digit[4]) * 0.1
        speed += float(number_in_digit[5]) * 0.01
    elif len(median) == 10:  # 2-digit number
        number_in_digit = median[:5]
        speed += float(number_in_digit[0]) * 10
        speed += float(number_in_digit[1])
        speed += float(number_in_digit[3]) * 0.1
        speed += float(number_in_digit[4]) * 0.01
    else:  # 1-digit number
        number_in_digit = median[:4]
        speed += float(number_in_digit[0])
        speed += float(number_in_digit[2]) * 0.1
        speed += float(number_in_digit[3]) * 0.01

    return speed


@app.route('/')
def hello_world():  # put application's code here
    group.run(verbose=True, json_output=True, timeout=TIMEOUT)
    median = str(group.median)
    pur_median = formating(median)
    response = jsonify({"speed": pur_median})

    return response


if __name__ == '__main__':
    app.run()
