import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/swaphedge', methods=['POST'])
def evaluate_swapHedge():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    previous = 0
    output = 0
    # for test_cases in data:
    output = data.get("accu_order") - previous
    previous = data.get("accu_order")

    logging.info("result : {}".format(output))

    return json.dumps({'output': int(output)})

