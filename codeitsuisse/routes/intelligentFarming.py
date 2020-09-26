import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluate_gmo():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    id = data['runId']
    sequences = data['list']
    output = {}
    output['runId'] = id
    output['list'] = []
    for sequence in sequences:
        seq_id = sequence['id']
        gene_seq = sequence['geneSequence']
        gene_result = {}
        gene_result['id'] = seq_id

        gene_len = len(gene_seq)
        a_count = 0
        c_count = 0
        g_count = 0
        t_count = 0
        for char in gene_seq:
            if char == 'A':
                a_count += 1
            elif char == 'C':
                c_count += 1
            elif char == 'G':
                g_count += 1
            elif char == 'T':
                t_count += 1
        
        num_cc = 0
        num_acgt = min(a_count, c_count, g_count, t_count)
        if num_acgt % 2 != 0 and c_count % 2 == 0:
            num_acgt -= 1
        num_cc = math.floor((c_count-num_acgt)/2)     

        new_seq = ''
        a_inserted = False
        while len(new_seq) < gene_len:
            if a_inserted == False:
                if a_count >= 2:
                    if num_acgt > 0:
                        new_seq += 'A'
                        a_count -= 1
                    else:
                        new_seq += 'AA'
                        a_count -= 2
                elif a_count == 1:
                    new_seq += 'A'
                    a_count -= 1
                a_inserted = True
            else:
                if num_acgt > 0:
                    new_seq += 'CGT'
                    c_count -= 1
                    g_count -= 1
                    t_count -= 1
                    num_acgt -= 1
                elif num_cc > 0:
                    new_seq += 'CC'
                    num_cc -= 1
                    c_count -= 2
                elif c_count > 0:
                    new_seq += 'C'
                    c_count -=1
                elif g_count > 0:
                    new_seq += 'G'
                    g_count -=1
                elif t_count > 0:
                    new_seq += 'T'
                    t_count -=1

                a_inserted = False  

        gene_result['geneSequence'] = new_seq
        output['list'].append(gene_result)
    logging.info("My result :{}".format(output))
    return jsonify(output)