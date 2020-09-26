import logging
import json
import heapq

from flask import request, jsonify;
from queue import Queue
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def compare(counter, bitmask, value):
    temp = bitmask
    count = 0
    counter += 1
    while counter>0:
        if(temp%2==1):
            counter-=1
            if(counter==0):
                break
        count+=1
        temp = temp >> 1   
       
    return (value[len(value)-1-count] == 'Y', count)    

def findExpected(num_values, num_operations, values):
    poss = [0] * num_operations
    total = [0] * num_operations
    q = Queue()
    q.put(((1<<num_values)-1, 0))
    while(not q.empty()):
        fr = q.get()
        bitmask = fr[0]
        numOps = fr[1]
        
        if(numOps >= num_operations):
            break
        for i in range(num_values-numOps):
            
            poss[numOps] += 1
            total[numOps] += 1
            (cond, pos) = compare(i, bitmask, values)
            
            if cond:
                q.put((bitmask & ~(1<<pos), fr[1] + 1))
            else:
                (cond, pos) = compare(num_values - numOps - i - 1, bitmask, values)
                if cond:
                    q.put((bitmask & ~(1<<pos), fr[1] + 1))
                else:
                    poss[numOps] -= 1
                    

    expected = 0
    for i in range(num_operations):
        if total[i]:
            expected += poss[i] / total[i]

    return expected  

@app.route('/yin-yang', methods=['POST'])
def evaluate_yinYang():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    number_of_elements = data.get("number_of_elements")
    number_of_operations = data.get("number_of_operations")
    elements = data.get("elements")
    result = findExpected(number_of_elements, number_of_operations, elements) 
    logging.info("My result :{}".format(result))
    return f"{result:.{10}f}"
