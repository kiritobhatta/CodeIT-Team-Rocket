import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def olympiad(days,books):
    import math
    days = sorted(days, reverse=True)
    # dimensions of dp:
    #   index reached so far
    #       leftover so far -> length, [nums]
    target = days[0]
    answer = 0
    while days:
        target = days.pop()
        # print(books)
        dp = {}
        for x in range(len(books)+1):
            dp[x] = {}

        dp[0][target] = (0, [])

        for index, element in enumerate(books):
            index += 1
            for sub_indice in range(index):
                for sub_leftover in dp[sub_indice]:
                    sub_len, sub_elems = dp[sub_indice][sub_leftover]
                    cur_leftover = sub_leftover - element
                    if cur_leftover >= 0:
                        if cur_leftover not in dp[index]:
                            dp[index][cur_leftover] = (
                                sub_len+1, sub_elems+[index-1])
                        else:
                            if sub_len+1 < dp[index][cur_leftover][0]:
                                dp[index][cur_leftover] = (
                                    sub_len+1, sub_elems+[index-1])
        min_val = math.inf
        output = []
        # for indice, leftovers in dp.items():
        #     print()

        # print(sorted(, reverse=True))
        max_val_count = -math.inf
        min_val_leftovers = math.inf
        for index in dp:
            for leftovers in dp[index]:
                count = dp[index][leftovers][0]
                if count > max_val_count:
                    max_val_count = count
                    min_val_leftovers = leftovers
                    indices = dp[index][leftovers][1]
                elif count == max_val_count:
                    if leftovers < min_val_leftovers:
                        indices = dp[index][leftovers][1]
                        min_val_leftovers = leftovers

        answer += max_val_count
        # print(max_val_count, min_val_leftovers, indices)
        new_arr = []
        x = 0
        for ind, elem in enumerate(books):

            if x < len(indices) and ind == indices[x]:
                x += 1
            else:
                new_arr.append(elem)

        books = new_arr
    return answer

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateOB():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    days = data["days"]
    books = data["books"]
    result = {"optimalNumberOfBooks" : olympiad(days,books)}
    logging.info("My result :{}".format(result))
    return json.dumps(result)