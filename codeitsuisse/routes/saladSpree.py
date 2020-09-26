import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluate_salad():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = salad_spree(data.get("number_of_salads"), data.get("salad_prices_street_map"))
    logging.info("result : {}".format(result))

    return json.dumps({'result': int(result)})




def salad_spree(num, list_array):
    index = 0
    min_value = 0
    temp_value = 0
    for array in list_array:
        for elements in range(len(array)-num+1):
            index = 0
            temp_value = 0
            for loop in range(num):
                if array[elements+loop] != "X":
                    temp_value += int(array[elements+loop])
                else:
                    break
                index += 1
                
            if index == num and (min_value == 0 or min_value > temp_value):
                min_value = temp_value
    
    return min_value