import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitbasket():
    dataByteString = request.get_data()
    dataString = dataByteString.decode('utf-8')
    data = json.loads(dataString)
    logging.info("data sent for evaluation {}".format(data))

    appleAmount = data.get("maApple")
    watermelonAmount = data.get("maWatermelon")
    bananaAmount = data.get("maBanana")

    appleWeight = 10
    watermelonWeight = 20
    bananaWeight = 30

    result = appleAmount*appleWeight + watermelonAmount*watermelonWeight + bananaAmount*bananaWeight

    logging.info("My result :{}".format(result))
    return result
