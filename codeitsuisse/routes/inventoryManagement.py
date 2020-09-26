import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
from itertools import islice

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def inventoryManagement():
    data = request.get_json()[0]
    logging.info("data sent for evaluation {}".format(data))
    
    searchTerm = data.get("searchItemName")

    items = data.get("items")

    scoreDict = {}

    for item in items:
        score = minDistance(searchTerm, item)
        if score in scoreDict:
            scoreDict[score].append(item)
        else:
            scoreDict[score] = [item]

    # retrieve top 10
    answer = []
    for key in reversed(list(scoreDict.keys())):
        terms = scoreDict[key]
        terms.sort()
        for term in terms:
            answer.append(term)
            if len(terms) == 10:
                return json.dumps(answer)

    logging.info("data sent for evaluation {}".format(answer))

    return json.dumps(answer)

def minDistance(word1, word2):
    n = len(word1)
    m = len(word2)
    
    if n * m == 0:
        return n + m
    
    d = [ [0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            left = d[i - 1][j] + 1
            down = d[i][j - 1] + 1
            left_down = d[i - 1][j - 1] 
            if word1[i - 1] != word2[j - 1]:
                left_down += 1
            d[i][j] = min(left, down, left_down)
    
    return d[n][m]

# @app.route('/inventory-management', methods=['POST'])
# def evaluate_inventory():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     final = []
#     for test_case in data:
#         result = Management(test_case["searchItemName"], test_case["items"])
#         final.append({'searchItemName': test_case["searchItemName"], 'searchResult': result})
#     return jsonify(final)


# def Management(name, list_array):
#     ordered_dict = {}
#     sorted_list = sorted(list_array, key=str.lower)
#     for word in sorted_list:
#         new_word = ""
#         array_char_index = 0
#         num = 0
#         for name_char_index in range(len(name)):
#             if name[name_char_index] == " ":
#                 while (array_char_index < len(word) and word[array_char_index] != " "):
#                     new_word += "+" + word[array_char_index]
#                     array_char_index += 1
#                 continue
#             if array_char_index < len(word) and word[array_char_index] == " ":
#                 array_char_index += 1
#                 new_word += " "
#             if array_char_index < len(word):
#                 if str(name[name_char_index]).lower() == str(word[array_char_index]).lower():
#                     new_word += name[name_char_index]
#                     array_char_index += 1
#                 else:
                    
#                     if name_char_index+1 < len(name) and array_char_index+1 < len(word) and str(name[name_char_index+1]).lower() == str(word[array_char_index+1]).lower():
#                         new_word += word[array_char_index]
#                         array_char_index += 1
#                         num += 1
#                     elif array_char_index+1 < len(word) and str(name[name_char_index]).lower() == str(word[array_char_index+1]).lower():
#                         if word[array_char_index+1] != " ":
#                             new_word += "+" + word[array_char_index]
#                             num += 1
#                         array_char_index += 1
#                     else:
#                         new_word += "-" + name[name_char_index]
#                         num += 1
#             else:
#                 new_word += "-" + name[name_char_index]
#                 num += 1
#         if array_char_index < len(word):
#             for temp in range(len(word)-array_char_index):
#                 new_word += "+" +  word[array_char_index]
#                 array_char_index += 1
#                 num += 1
#         ordered_dict[new_word] = num
#     ordered_dict.keys()
#     return list(islice(ordered_dict, 10))
