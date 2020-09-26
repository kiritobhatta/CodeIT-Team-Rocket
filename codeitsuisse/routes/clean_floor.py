import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluate_clean_floor():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests");
    ans = {}
    for key in tests:
        ans[key] = clean_floor(tests[key]['floor'])

    logging.info("My result :{}".format(ans))
    return json.dumps({"answers": ans})




def clean_floor1(list_array):
    start_index = 0
    end_index = len(list_array) - 1

    






def clean_floor(list_array):
    start_index = 0
    current_index = 0
    moves = 0

    if (len(list_array) == 1):
        moves = list_array[0]
    else:
        while (start_index != len(list_array)):
            
            if current_index != start_index:
                current_index = start_index
            else:
                if (current_index >= len(list_array)-1):
                    current_index = start_index - 1
                else:
                    current_index = start_index + 1
            print(current_index)
            moves += 1
            if list_array[current_index] > 0:
                list_array[current_index] -= 1
            else:
                list_array[current_index] += 1

            if start_index >= len(list_array)-2 and list_array[start_index] == 0 and list_array[current_index] == 0:
                break
            elif (list_array[start_index] == 0 and start_index != len(list_array)-1):
                start_index += 1
        
    return moves