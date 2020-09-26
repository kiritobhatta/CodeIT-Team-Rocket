import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluateFarming():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    runId = data.get("runId")
    genomes = data.get("list")
    resultList = []

    for genome in genomes:
        genseq = genome["geneSequence"]
        resultList.append({"id": genome["id"], "geneSequence": maximizeDRI(genseq)})

    result = {"runId": runId, "list": resultList}
    logging.info("My result :{}".format(result))
    return jsonify(result)

def maximizeDRI(genseq):
    hash = {"A": 0, "C": 0, "G": 0, "T": 0}
    for i in genseq:
        if (i == "A"): hash["A"] += 1
        elif (i == "C"): hash["C"] += 1
        elif (i == "G"): hash["G"] += 1
        elif (i == "T"): hash["T"] += 1

    DRIscore = 0
    greedyArr = [""] * (hash["A"] + hash["C"] + hash["G"] + hash["T"])

    for i in range(len(genseq)):
        while hash["C"] > 1:
            greedyArr[i] = "C"
            greedyArr[i+1] = "C"
            i += 2
            if hash["A"] >= 1:
                greedyArr[i] = "A"
                greedyArr[i+1] = "A"
                hash["A"] -= 2
                i += 2
            hash["C"] -= 2
            DRIscore += 50

        while (hash["A"] >= 1 and hash["C"] >= 1 and hash["G"] >= 1 and hash["T"] >= 1):
            greedyArr[i] = "A"
            hash['A'] -= 1
            greedyArr[i+1] = "C"
            hash['C'] -= 1
            greedyArr[i+2] = "G"
            hash['G'] -= 1
            greedyArr[i+3] = "T"
            hash['T'] -= 1
            DRIscore += 10
            i += 4

        if (hash["C"] == 1):
            greedyArr[i] = "C"
            hash["C"] -= 1
            i += 1

        if hash["A"] >= 1:
            greedyArr[i] = "A"
            greedyArr[i+1] = "A"
            hash["A"] -= 2
            i += 2

        while (hash["G"] >= 0):
            greedyArr[i] = "G"
            hash["G"] -= 1
            i += 1
            if hash["A"] >= 1:
                greedyArr[i] = "A"
                greedyArr[i+1] = "A"
                hash["A"] -= 2
                i += 2

        while (hash["T"] >= 0):
            greedyArr[i] = "T"
            hash["T"] -= 1
            i += 1
            if hash["A"] >= 1:
                greedyArr[i] = "A"
                greedyArr[i+1] = "A"
                hash["A"] -= 2
                i += 2

        for i in range(len(greedyArr)-2):
            if greedyArr[i] == "A" and greedyArr[i+1] == "A" and greedyArr[i+2] == "A":
                DRIscore -= 20
                if i+2 != len(greedyArr)-1: i += 3

        if DRIscore <= 0:
            return genseq
        else:
            greedStr = ""
            for i in greedyArr:
                greedStr += i

    return greedStr