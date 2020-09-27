import logging
import json

from flask import request, jsonify;
import xml.etree.ElementTree as ET

from codeitsuisse import app;

logger = logging.getLogger(__name__)
CIRCLE = "{http://www.w3.org/2000/svg}circle"
POLYLINE = "{http://www.w3.org/2000/svg}polyline"


def solvewater(circles, buckets, pipes):

    IMG_SIZE = 0
    for b in buckets:
        for bb in b:
            IMG_SIZE = max(IMG_SIZE, bb[0], bb[1])

    for b in pipes:
        for bb in b:
            IMG_SIZE = max(IMG_SIZE, bb[0], bb[1])

    img = [[-1 for i in range(IMG_SIZE+5)] for j in range(IMG_SIZE+5)]
    G = [list() for j in range(len(buckets)+5)]
    area = [0 for j in range(len(buckets)+5)]


    for b in range(len(buckets)):

        buc = buckets[b]
        left, right, top, bottom = buc[0][0], buc[2][0], buc[0][1], buc[2][1]

        if(left > right):
            buc[0], buc[2] = buc[2], buc[0]
            buc[1], buc[3] = buc[3], buc[1]
            left, right = right, left

        for i in range(top, bottom+1):
            
            img[left][i] = b
            img[right][i] = b
        for i in range(left, right+1):
            img[i][bottom] = b
        area[b] = (right-left-1)*(bottom-top)
        

    for pipe in pipes:
        up, down = pipe
        src, tgt = -1, -1
        for i in range(up[1], -1, -1):
            if(img[up[0]][i] != -1):
                src = img[up[0]][i]
                break
        for i in range(down[1], IMG_SIZE):
            if(img[down[0]][i] != -1):
                tgt = img[down[0]][i]
                break
        if(src != -1 and tgt != -1):
            G[src].append(tgt)

    startbuc = -1
    for i in range(circles[1], IMG_SIZE):
        if(img[circles[0]][i] != -1):
            startbuc = img[circles[0]][i]
            break

    for b in range(len(buckets)):
        buc = buckets[b]
        left, right, top, bottom = buc[0][0], buc[2][0], buc[0][1], buc[2][1]
        tgt = -1

        for i in range(bottom+1, IMG_SIZE):
            if(img[left][i] != -1):
                tgt = img[left][i]
                break

        if(tgt != -1):
            G[b].append(tgt)

        tgt = -1
        
        for i in range(bottom+1, IMG_SIZE):
            if(img[right][i] != -1):
                tgt = img[right][i]
                break
        
        if(tgt != -1):
            G[b].append(tgt)


    if(startbuc == -1):
        return 0
        ##############################

    visited = [0 for j in range(len(buckets)+5)]
    def dfs(v):
        visited[v] = 1
        for to in G[v]:
            if visited[to]==0:
                dfs(to)
            
    img = [[-1 for i in range(IMG_SIZE+5)] for j in range(IMG_SIZE+5)]
    for b in range(len(buckets)):
        buc = buckets[b]
        left, right, top, bottom = buc[0][0], buc[2][0], buc[0][1], buc[2][1]
        for j in range(top, bottom):
            for i in range(left+1, right):
                if (img[i][j]==-1) or (img[i][j]!=-1 and area[img[i][j]]<area[b]):
                    img[i][j] = b

    dfs(startbuc)

    ans =0

    for i in range(IMG_SIZE):
        for j in range(IMG_SIZE):
            if img[i][j]!=-1 and visited[img[i][j]]==1:
                    ans += 1



    print(visited)    
    print(G)
    return ans


@app.route('/bucket-fill', methods=['POST'])
def bucket_fill():
    data = request.get_data();
    root = ET.fromstring(data)
    logging.info("tree {}".format(root))
    children = []
    for child in root.iter('*'):
        children.append(child) 

    circles = (0,0)
    buckets = []
    pipes = []

    for child in children:
        if child.tag == CIRCLE:
            circles = (int(child.attrib['cx']), int(child.attrib['cy']))
        elif child.tag == POLYLINE:
            points = child.attrib['points'].split()
            if len(points) == 2:
                pipe = []
                for point in points:
                    x, y = map(int,point.split(','))
                    pipe.append((x,y))
                pipes.append(pipe)
            
            elif len(points) == 4:
                bucket = []
                for point in points:
                    x, y = map(int, point.split(','))
                    bucket.append((x,y))
                buckets.append(bucket)

    logging.info("circles: {}".format(circles))
    logging.info("buckets: {}".format(buckets))
    logging.info("pipes: {}".format(pipes))
                

    
    # print(data)
    # logging.info("data sent for evaluation {}".format(data))
    # data.sort() 

    result = {'result': solvewater(circles, buckets, pipes)}
    logging.info("My result :{}".format(result))
    return jsonify(result)


