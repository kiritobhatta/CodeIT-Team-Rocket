import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluate_gmo():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    runId = data.get("runId")
    lst = data.get("list")
    ans = []

    for el in lst:
        seq = el["geneSequence"]
        charCount = {"A":0,"C":0,"G":0,"T":0}
        for char in seq:
            charCount[char] += 1
        sorted_seq = []
        cc_count = 0
        acgt_count = 0
        while charCount["A"] > 0 and charCount["C"] > 0 and charCount["G"] > 0 and charCount["T"] > 0:
            sorted_seq.append("ACGT")
            charCount["A"] -= 1
            charCount["C"] -= 1
            charCount["G"] -= 1
            charCount["T"] -= 1
            acgt_count += 1
        while charCount["C"] > 1:
            sorted_seq.append("CC")
            charCount["C"] -= 2
            cc_count += 1
        for k,v in charCount.items():
            if k != "A":
                for i in range(v):
                    sorted_seq.append(k)
        for count in range(acgt_count):
            if charCount["A"] > 0:
                sorted_seq.insert(cc_count*2 + count*2, "A")
                charCount["A"] -= 1
        for count in range(cc_count):
            if charCount["A"] > 1:
                sorted_seq.insert(count*2, "AA")
                charCount["A"] -= 2
            elif charCount["A"] == 1:
                sorted_seq.insert(count*2, "AA")
                charCount["A"] -= 1
        count = 0
        while charCount["A"] > 0:
            if charCount["A"] == 1:
                sorted_seq.insert(cc_count*2 + acgt_count*2 + count*2, "A")
                charCount["A"] -= 1
            else:
                sorted_seq.insert(cc_count*2 + acgt_count*2 + count*2, "AA")
                charCount["A"] -= 2
            count += 1

        ans.append({"id":el["id"], "geneSequence":"".join(sorted_seq)})    

    result = {"runId":runId, "list":ans}
    logging.info("My result :{}".format(result))
    return jsonify(result)