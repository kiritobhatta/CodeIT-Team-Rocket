import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluateCleanFloor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests")
    final = {}

    for testNum in tests:
        moves = cleanFloor(testNum, tests[testNum]["floor"])
        final[testNum] = moves

    result = {}
    result["answers"] = final

    logging.info("My result :{}".format(result))
    # return json.dumps(result)
    return jsonify(result)

def changeDirt(num):
    if num > 0:
        num -= 1
        return num
    return num+1

def update_array(array, start, end, flag):
    for count in range(end - start):
        if not flag:
            index = start + count + 1
        else:
            index = end - count - 1
        if array[index] > 0:
            array[index] -= 1
        else:
            array[index] += 1
    return array

def cleanFloor(testNum, lst): 
    moves = 0
    cleaned_floor = [0 for pos in lst]
    states = [(0, lst)]

    while states:
        current_state = states.pop(0)
        floorRight = current_state[1]

        if floorRight == cleaned_floor:
            break

        floorLeft = floorRight[:]
        idx = current_state[0]

        if idx < len(lst) - 1:
            floorRight[idx + 1] = changeDirt(floorRight[idx + 1])
            states.append(tuple((idx + 1, floorRight)))
        
        if idx > 0:
            floorLeft[idx - 1] = changeDirt(floorLeft[idx - 1])
            states.append(tuple((idx - 1, floorLeft)))

        moves += 1

    return moves
    
def clean_floor1(list_array):
    start_index = 0
    end_index = len(list_array) - 1
    flag = False
    moves = 0
    while start_index != end_index:
        if flag:
            while list_array[start_index] == 0 and start_index <= len(list_array) - 1 and start_index != end_index:
                start_index += 1
        else:
            while list_array[end_index] == 0 and end_index >= 0 and start_index != end_index:
                end_index -= 1
        list_array = update_array(list_array, start_index, end_index, flag)
        moves += end_index - start_index
        flag = not flag
            
    if list_array[start_index] != 0:
        if list_array[start_index] % 2 == 1:
            moves += list_array[start_index] * 2 + 1
        else:
            moves += (list_array[start_index]) * 2
    return moves



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