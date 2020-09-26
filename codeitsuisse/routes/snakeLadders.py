import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/slsm', methods=['POST'])
def evaluate_slsm():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    boardSize = data['boardSize']
    players = data['players']
    jumps = data['jumps']

    snakes = {}
    ladders = {}
    smokes = set()
    mirrors= set()
    for jump in jumps:
        jump = jump.split(':')
        if jump[1] == '0':
            smokes.add(int(jump[0]))
        if jump[0] == '0':
            mirrors.add(int(jump[1]))
        if int(jump[0]) > int(jump[1]):
            snakes[int(jump[0])] = int(jump[1])
        if int(jump[0]) < int(jump[1]):
            ladders[int(jump[0])] = int(jump[1])

    ## all start at 0
    player_pos = [1] * players
    last = players-1
    dice_rolls = []

    def go_next(cur_pos, smoky):
        best_roll = 0
        mirror = False
        smoke = False
        best_pos = 0
        for i in range(1,7):
            if smoky:
                i = -i
            new_pos = cur_pos + i
            if new_pos == boardSize:
                best_pos = boardSize
                best_roll = i
                mirror = False
                smoke = False
                break
            elif new_pos in ladders.keys():
                new_pos = ladders[new_pos]
                if new_pos > best_pos:
                    best_pos = new_pos
                    best_roll = i
                    mirror = False
                    smoke = False
            elif new_pos in mirrors:
                mirror = True
                if new_pos > best_pos:
                    best_pos = new_pos
                    best_roll = i
                    smoke = False
            elif new_pos not in set(snakes.keys()).union(smokes):
                if new_pos > best_pos:
                    best_pos = new_pos
                    best_roll = i
                    mirror = False
                    smoke = False
            elif new_pos in smokes:
                smoke = True
                if new_pos > best_pos:
                    best_pos = new_pos
                    best_roll = i
                    mirror = False
            elif new_pos in snakes.keys():
                new_pos = snakes[new_pos]
                if new_pos > best_pos:
                    best_pos = new_pos
                    best_roll = i
                    mirror = False
                    smoke = False
        if smoky:
            best_roll = -best_roll
        return best_pos, best_roll, mirror, smoke
        
    while player_pos[last] < boardSize:
        dice_rolls += [1] * (last)
        best_pos, best_roll, mirror, smoke = go_next(player_pos[last], False)
        player_pos[last] = best_pos
        print(player_pos[last])
        dice_rolls.append(best_roll)
        while mirror or smoke:
            if mirror:
                best_pos, best_roll, mirror, smoke = go_next(player_pos[last], False)
                player_pos[last] = best_pos
                dice_rolls.append(best_roll)
            if smoke:
                player_pos[last] = best_pos
                dice_rolls.append(best_roll)
                best_pos, best_roll, mirror, smoke = go_next(player_pos[last], True)
            print(player_pos[last])
            
    logging.info("My result :{}".format(dice_rolls))
    return json.dumps(dice_rolls)