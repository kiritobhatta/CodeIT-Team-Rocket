import logging
import json
import heapq

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def slsmsolution(boardSize,players,jumps):
    G = {i:{} for i in range(1,boardSize+1)}
    laddersnake = {}
    isjumppoint = [0 for i in range(boardSize+5)]

    for jp in jumps:
        s, e = jp.split(':')
        s, e = int(s), int(e)
        if(s == 0):
            for i in range(1,7):
                G[e][s+i] = 0
            isjumppoint[e] = 1
        elif(e == 0):
            for i in range(1,7):
                G[s][s-i] = 0
            isjumppoint[s] = 1
        else:
            G[s][e] = 0
            laddersnake[s] = e
            isjumppoint[s] = 1

    for i in range(1, boardSize):
        if(isjumppoint[i]):
            continue
        for j in range(1,7):
            if(i+j > boardSize):
                break
            G[i][i+j] = 1



    def calculate_distances(graph, starting_vertex):
        distances = {vertex: float('infinity') for vertex in graph}
        distances[starting_vertex] = 0
        previous = {vertex: -1 for vertex in graph}

        pq = [(0, starting_vertex)]
        while len(pq) > 0:
            current_distance, current_vertex = heapq.heappop(pq)
            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in graph[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))

        return distances, previous


    distances, previous = calculate_distances(G, 1)

    ans = []
    path = [boardSize]
    now = boardSize
    while True:
        pre = previous[now]
        if(pre==-1):
            break
        if(laddersnake.get(pre,0)!=now):
            ans.append(abs(now-pre))
        now = pre
        path.append(now)

    print(path)

    tem = []
    if(ans[0] == 1):
        ans[1] -= 1
    else:
        ans[0] -= 1

    for x in ans[::-1]:
        for y in range(players):
            tem.append(x)

    tem[-1] += 1

    return tem

@app.route('/slsm', methods=['POST'])
def evaluate_slsm():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    boardSize = data.get("boardSize")
    players = data.get("players")
    jumps = data.get("jumps")
    result = slsmsolution(boardSize,players,jumps)
    logging.info("My result :{}".format(result))
    return json.dumps(result)

