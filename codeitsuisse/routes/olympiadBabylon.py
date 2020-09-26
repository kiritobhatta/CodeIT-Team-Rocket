import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

from ortools.linear_solver import pywraplp



def create_data_model(w,b):
    """Create the data for the example."""
    data = {}
    weights = w
    values =  [1 for i in weights]
    data['weights'] = weights
    data['values'] = values
    data['items'] = list(range(len(weights)))
    data['num_items'] = len(weights)
    num_bins = len(b)
    data['bins'] = list(range(num_bins))
    data['bin_capacities'] = b
    return data




def solver(w,b):
    data = create_data_model(w,b)

    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('multiple_knapsack_mip', 'CBC')

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    objective = solver.Objective()

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return int(objective.Value())

def solve(data):
    bk,dy=data['books'],data['days']
    bk.sort()
    dy.sort()
    if (len(bk)<50):
        return solver(bk,dy)
    nb,nd=len(bk),len(dy)
    ans=0
    for i in range(nb):
        tmp=bk[:i+1]
        dd=dy[:]
        mi,cur,pp=1000000000,0,[]
        for x in range(nd):
            for j in range(len(dd)):
                d=dd[j]
                dp=[0 for i in range(d+1)]
                dp[0]=1
                ind=[[] for i in range(d+1)]
                for k in range(len(tmp)):
                    for tot in range(d,tmp[k]-1,-1):
                        if dp[tot]==0 and dp[tot-tmp[k]]:
                            dp[tot]=1
                            ind[tot]=[c for c in ind[tot-tmp[k]]]
                            ind[tot].append(k)
                for k in range(d,0,-1):
                    if dp[k]:
                        if d-k<=mi:
                            mi=d-k
                            cur=d
                            pp=[y for y in ind[k][::-1]]
                        break
            for x in pp:
                tmp.pop(x)
            dd.remove(cur)
            mi=1000000000
            if not tmp:
                break;
        if not tmp:
            ans=i+1
        else:
            return ans  
    return nb

@app.route('/olympiad-of-babylon', methods=['POST'])
def olympiad_of_babylon():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result = solve(data)
    result={'optimalNumberOfBooks':result}
    logging.info("My result :{}".format(result))
    return json.dumps(result);