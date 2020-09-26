import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def clean():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests");
    ans = {}
    for key in tests:
        ans[key] = clean_floor(tests[key]['floor'])

    logging.info("My result :{}".format(ans))
    return json.dumps({"answers": ans});


def clean_floor(a):
    # a is an array of binary digits e.g., [0,1,1,1]
    i = 0
    n = len(a)
    d = sum(a)
    num_moves = 0

    if d == 0:
        return 0

    while sum(a) > 0:
        if sum(a[i:]) > 0:
            a[i] = 1-a[i]
            num_moves += 1

            if sum(a[i+1:])==0:
                i-=1
            else:
                i += 1

        else:
            if sum(a[:i]) > 0:
                a[i] = 1-a[i]
                num_moves += 1
                i -= 1
        if num_moves > 1000:
            break

    return num_moves
