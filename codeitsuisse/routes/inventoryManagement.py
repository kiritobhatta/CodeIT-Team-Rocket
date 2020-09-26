import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
from itertools import islice

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluate_inventory():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = Management(data[0]["searchItemName"], data[0]["items"])
    dict_value = {'searchItemName': data[0]["searchItemName"], 'searchResult': result}
    return json.dumps([dict_value])


def Management(name, list_array):
    ordered_dict = {}
    sorted_list = sorted(list_array, key=str.lower)
    for word in sorted_list:
        new_word = ""
        array_char_index = 0
        num = 0
        for name_char_index in range(len(name)):
            if name[name_char_index] == " ":
                while (array_char_index < len(word) and word[array_char_index] != " "):
                    new_word += "+" + word[array_char_index]
                    array_char_index += 1
                continue
            if array_char_index < len(word) and word[array_char_index] == " ":
                array_char_index += 1
                new_word += " "
            if array_char_index < len(word):
                if str(name[name_char_index]).lower() == str(word[array_char_index]).lower():
                    new_word += name[name_char_index]
                    array_char_index += 1
                else:
                    
                    if name_char_index+1 < len(name) and array_char_index+1 < len(word) and str(name[name_char_index+1]).lower() == str(word[array_char_index+1]).lower():
                        new_word += word[array_char_index]
                        array_char_index += 1
                        num += 1
                    elif array_char_index+1 < len(word) and str(name[name_char_index]).lower() == str(word[array_char_index+1]).lower():
                        if word[array_char_index+1] != " ":
                            new_word += "+" + word[array_char_index]
                            num += 1
                        array_char_index += 1
                    else:
                        new_word += "-" + name[name_char_index]
                        num += 1
            else:
                new_word += "-" + name[name_char_index]
                num += 1
        if array_char_index < len(word):
            for temp in range(len(word)-array_char_index):
                new_word += "+" +  word[array_char_index]
                array_char_index += 1
                num += 1
        ordered_dict[new_word] = num
    ordered_dict.keys()
    return list(islice(ordered_dict, 10))
