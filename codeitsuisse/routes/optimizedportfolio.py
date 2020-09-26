import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import numpy as np

logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_portfolio():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputs = data.get('inputs')
    ans = []
    print(type(inputs))
    for inp in inputs:
        print("Hello")
        port = inp['Portfolio']
        indf= inp['IndexFutures']
        ans.append(opt_portfolio(port, indf))

    logging.info("My result :{}".format(ans))
    return json.dumps({"outputs": ans})


def opt_portfolio(portfolio, index_futures):
    if_vol = np.array([ind['FuturePrcVol'] for ind in index_futures])
    if_rho = np.array([ind['CoRelationCoefficient'] for ind in index_futures])
    spot_price_vol = portfolio["SpotPrcVol"]

    hedge_ratios = np.round(if_rho * spot_price_vol / if_vol, 3)
    idx = np.argmin(hedge_ratios)
    # print(hedge_ratios)
    hr = hedge_ratios[idx]
    if sum(hedge_ratios==hr)>1:
        # print(if_vol)
        vol = np.min(if_vol[hedge_ratios==hr])
        idx = np.where(if_vol == vol)[0][0]
        hr = hedge_ratios[idx]

    num_futures = hr * portfolio['Value'] /  (index_futures[idx]['IndexFuturePrice'] * index_futures[idx]['Notional'])
    output = {'HedgePositionName': index_futures[idx]['Name'],
             'OptimalHedgeRatio': hr,
             'NumFuturesContract': int(round(num_futures))}
    return output

def opt_portfolio1(portfolio, index_futures):
    if_vol = np.array([ind['FuturePrcVol'] for ind in index_futures])
    if_rho = np.array([ind['CoRelationCoefficient'] for ind in index_futures])
    spot_price_vol = portfolio["SpotPrcVol"]

    hedge_ratios = if_rho * spot_price_vol / if_vol
    idx = np.argmin(hedge_ratios)
    hr = np.round(hedge_ratios[idx],3)
    num_futures = hr * portfolio['Value'] / (index_futures[idx]['IndexFuturePrice'] * index_futures[idx]['Notional'])
    output = {'HedgePositionName': index_futures[idx]['Name'],
             'OptimalHedgeRatio': hr,
             'NumFuturesContract': int(round(num_futures))}
    return output