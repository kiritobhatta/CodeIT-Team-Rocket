import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/swaphedge', methods=['POST'])
def evaluate_swapHedge():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    dict_new = {}
    # for test_cases in data:
    dict_new['output'] = data.get("order")

    logging.info("output : {}".format(dict_new['output']))

    return jsonify(dict_new)

