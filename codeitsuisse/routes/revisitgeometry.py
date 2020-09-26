import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def ev():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input");
    sc = data.get("shapeCoordinates")
    lc = data.get("lineCoordinates")
    result = revisit_geometry(sc, lc)

    logging.info("My result :{}".format(result))
    return json.dumps(result);

def revisit_geometry(shape_coords, line_coords):
    if len(line_coords)<2  or len(shape_coords)==0:
        return []

    n = len(shape_coords)
    out = []

    for j in range(len(line_coords)-1):
        l1 = line_coords[j]
        l2 = line_coords[j+1]
        for i in range(n-1):
            p1 = shape_coords[i]
            p2 = shape_coords[i+1]

            A = np.array([[p1['y']-p2['y'], p2['x']-p1['x']],[l1['y']-l2['y'], l2['x']-l1['x']]])
            if np.linalg.det(A) == 0:
                continue

            c1 = (p2['x']-p1['x'])* p1['y']-(p2['y']-p1['y'])*p1['x']
            c2 = (l2['x']-l1['x'])* l1['y']-(l2['y']-l1['y'])*l1['x']
            b = np.array([c1, c2])
            a = np.linalg.inv(A) @ b.T

            if a[0] > p1['x'] and a[0] > p2['x'] or a[1] > p1['y'] and a[1] > p2['y']:
                continue

            if a[0] < p1['x'] and a[0] < p2['x'] or a[1] < p1['y'] and a[1] < p2['y']:
                continue

            out.append({"x": a[0], "y": a[1]})
        p1 = shape_coords[0]
        p2 = shape_coords[-1]

        A = np.array([[p1['y']-p2['y'], p2['x']-p1['x']],[l1['y']-l2['y'], l2['x']-l1['x']]])
        if np.linalg.det(A) == 0:
            continue

        c1 = (p2['x']-p1['x'])* p1['y']-(p2['y']-p1['y'])*p1['x']
        c2 = (l2['x']-l1['x'])* l1['y']-(l2['y']-l1['y'])*l1['x']
        b = np.array([c1, c2])
        a = np.linalg.inv(A) @ b.T

        if a[0] > p1['x'] and a[0] > p2['x'] or a[1] > p1['y'] and a[1] > p2['y']:
            continue
        if a[0] < p1['x'] and a[0] < p2['x'] or a[1] < p1['y'] and a[1] < p2['y']:
            continue

        out.append({"x": a[0], "y": a[1]})

    return out


