import logging
import json
import heapq

from flask import request, jsonify;
from queue import Queue
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def check(i,bitmask,elements):
    b = bitmask
    count = 0
    # print(i)
    i += 1
    while i>0:
        if(b%2==1):
            i-=1
            if(i==0):
                break
        count+=1
        b = b >> 1   
    # print(elements, " --> ", count, elements[len(elements)-1-count])    
    return (elements[len(elements)-1-count] == 'Y', count)    

def ev(bitmask, elements):
    s = ""
    b = bitmask
    i = 0
    # print("---------")
    while b >= 1:
        # print(b)
        if(b%2 == 1):
            s += elements[len(elements) - 1 - i]
        i += 1
        b = b >> 1
    # print(s,bin(bitmask),elements,"<----")    
    return s        

def findExpected(number_of_elements, number_of_operations, elements):
    poss = [0] * (number_of_operations + 5)
    total = [0] * (number_of_operations + 5)
    map = {}
    q = Queue()
    q.put(((1<<number_of_elements)-1, 0))
    while(not q.empty()):
        fr = q.get()
        bitmask = fr[0]
        numOps = fr[1]
        shrt = ev(bitmask, elements)
        # print(shrt, map.keys())
        if shrt in map.keys():
            # print(shrt, map[shrt])
            poss[numOps] += map[shrt][0]
            total[numOps] += map[shrt][1]
        else:
            # print(bin(bitmask), numOps)
            p = 0
            t = 0
            if(numOps >= number_of_operations):
                break
            for i in range(number_of_elements-numOps):
                # print(i,"--", numOps)
                poss[numOps] += 1
                p += 1
                total[numOps] += 1
                t += 1
                (cond, pos) = check(i,bitmask,elements)
                # print(elements[len(elements)-1-pos], bin(bitmask), i)
                if cond:
                    q.put((bitmask & ~(1<<pos), fr[1] + 1))
                else:
                    (cond, pos) = check(number_of_elements - numOps - i -1,bitmask,elements)
                    if cond:
                        q.put((bitmask & ~(1<<pos), fr[1] + 1))
                    else:
                        poss[numOps] -= 1
                        p -= 1
            map[shrt] = (p,t)        

    expected = 0
    # print(poss)
    # print(total)
    for i in range(number_of_operations):
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
