import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluate_salad():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result = salad_spree(data.get("number_of_salads"), data.get("salad_prices_street_map"))
    logging.info("result: {}".format(result))
    return json.dumps(result);

def salad_spree(num, list_array):
    min_value = 0
    temp_value = 0
    for array in list_array:
        for elements in range(len(array)-2):
            if (array[elements] != 'X' and array[elements+1] != 'X' and array[elements+2] != 'X'):
                temp_value = int(array[elements]) + int(array[elements+1]) + int(array[elements+2])
                print(temp_value)
                if min_value == 0 or min_value > temp_value:
                    min_value = temp_value
    
    return min_value
