import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def supermarks(data):
  maze,start,end = data["maze"],data["start"],data["end"]
  vertices = {}
  def recurse(x,y,prev,point):
    if end[0]==x and end[1]==y:
      if (x,y) in vertices:
        vertices[(x,y)]=min(vertices[(x,y)],point)
      else:
        vertices[(x,y)]=point
    else:
      if (x,y) in vertices:
        if vertices[(x,y)]<=point:
          return
      vertices[(x,y)]=point
      if prev != "right" and x+1>0 and x+1<len(maze[0]) and y>0 and y<len(maze) and maze[y][x+1]!=1:
        recurse(x+1,y,"left",point+1)
      if prev != "left" and x-1>0 and x-1<len(maze[0]) and y>0 and y<len(maze) and maze[y][x-1]!=1:
        recurse(x-1,y,"right",point+1)
      if prev != "up" and x>0 and x<len(maze[0]) and y-1>0 and y-1<len(maze) and maze[y-1][x]!=1:
        recurse(x,y-1,"down",point+1)
      if prev != "down" and x>0 and x<len(maze[0]) and y+1>0 and y+1<len(maze) and maze[y+1][x]!=1:
        recurse(x,y+1,"up",point+1)
  recurse(start[0],start[1],"none",1)
  if (end[0],end[1]) in vertices:
    return vertices[(end[0],end[1])]
  else:
    return -1
    

@app.route('/supermarket', methods=['POST'])
def supermarrket():
  data = request.get_json()["tests"]
  logging.info("data sent for evaluation {}".format(data))
  result={'answers':{}}
  for da in data:
    ret = supermarks(data[da])
    result['answers'][da] = ret
  return jsonify(result)