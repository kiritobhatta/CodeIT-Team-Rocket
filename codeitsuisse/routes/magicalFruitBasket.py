import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitbasket():
    data = request.get_data();
    data = json.loads(data)
    
    logging.info("data sent for evaluation2 {}".format(data))
    # print("keys:",data.keys)
    weight1 = 11
    weight2 = 53
    weight3 = 30

    listNo = []
    for key in data.keys():
        listNo.append(data[key])

    result = (weight1*listNo[0]) + weight2*listNo[1] + weight3*listNo[2]
    logging.info("My result :{}".format(result))
    logging.info("List :{}".format(listNo))

    return (str(result));
