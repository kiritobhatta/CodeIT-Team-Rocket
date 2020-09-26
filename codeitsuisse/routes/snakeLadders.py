import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def slsm(boardSize, player, jumps):
    board = [i for i in range(boardSize + 1)]
    ans = []

    for jump in jumps:
        temp = jump.split(":")
        if int(temp[0]) == 0:
            board[int(temp[1])] = min(int(temp[1]) + 6, boardSize)
        elif int(temp[1]) == 0:
            board[int(temp[0])] = max(int(temp[0]) - 6, 0)
        elif int(temp[0]) > int(temp[1]):
            board[int(temp[1])] = int(temp[0])
        elif int(temp[0]) < int(temp[1]):
            board[int(temp[1])] = int(temp[1])

    print(board[290:])
    x = 0
    y = 0
    shortest_path = []

    while x != boardSize:
        next_6 = board[x + 1:x + 6 + 1]

        next_6_l = board[y + 1:y + 6 + 1]
        best_choice_l = next_6_l.index(min(next_6_l)) + 1
        for _ in range(player - 1):
            shortest_path.append(best_choice_l)
        y = min(next_6_l)

        best_choice = next_6.index(max(next_6)) + 1
        shortest_path.append(best_choice)
        x = max(next_6)
        ans.append(x)
    print(ans)
    return shortest_path

@app.route('/slsm', methods=['POST'])
def evaluate_slsm():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    boardSize = data.get("boardSize")
    players = data.get("players")
    jumps = data.get("jumps")
    result = slsm(boardSize, players, jumps)
    logging.info("My result :{}".format(result))
    return jsonify(result)

