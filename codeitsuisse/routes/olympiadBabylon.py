import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

# def num_books_for_min(books_left, minute, books_read):
#     if len(books_left) == 1:
#         if books_left[0] > minute:
#             return [books_read]
#         else:
#             return [books_read + books_left]
#     if books_left[0] <= minute < books_left[1]:
#         return [books_read + books_left[:1]]
#     all_books_sets = [books_read]
#     max_books = len(books_read)
#     for i in range(len(books_left) - 1):
#         if books_left[i] <= minute:
#             books = num_books_for_min(books_left[i + 1:], minute - books_left[i], books_read + [books_left[i]])
#             if len(books[0]) > max_books:
#                 max_books = len(books[0])
#                 all_books_sets = books
#             elif len(books[0]) == max_books:
#                 all_books_sets += books
#     return all_books_sets


# def max_num_books(books_left, days):
#     max_ans = 0
#     for minute in days:
#         books = num_books_for_min(books_left, minute, [])
#         max_books = books[-1]
#         max_ans += len(max_books)
#         for i in max_books:
#             books_left.remove(i)
#     return max_ans

def optimal_books(day, books):
        
        dpDict = {}
        for n in range(day+1):
            dpDict[n] = set()

        for key in dpDict.keys():
            for index in range(len(books)):
                num = books[index]
                if key-num in dpDict and index not in dpDict[key-num]:
                    prevSet = dpDict[key-num]
                    if len(prevSet)+1 >= len(dpDict[key]):
                        dpDict[key] = prevSet.copy()
                        dpDict[key].add(index)
        
        largestSubset = dpDict[0]
        for key in reversed(list(dpDict.keys())):
            if len(dpDict[key]) != 0:
                return dpDict[key]

        return largestSubset

@app.route('/olympiad-of-babylon', methods=['POST'])
# def evaluateBabylon():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     no_books = data.get("numberOfBooks")
#     no_days = data.get("numberOfDays")


#     books_left = sorted(data.get("books"))
#     days = sorted(data.get("days"), reverse=True)

#     max_ans = max(
#         max_num_books(books_left.copy(), days),
#         max_num_books(books_left.copy(), days[::-1])
#     )
#     result = {"optimalNumberOfBooks": max_ans}

#     logging.info("My result :{}".format(result))
#     return jsonify(result)
def evaluateBabylon():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    books = data.get("books")
    days = data.get("days")
    no_days = data.get("numberOfDays")

    result = 0
    for i in range(no_days):
        
        bestDiff = float('inf')
        dayFound = 0
        bestSubset = set()
        for index in range(len(days)):
            day = days[index]
            if day != 0:
                subset = optimal_books(day, books)
                totalTimeSpent = 0
                for bookIndex in subset:
                    totalTimeSpent += books[bookIndex]
                diff = day - totalTimeSpent
                if diff < bestDiff:
                    bestDiff = diff
                    bestSubset = subset
                    dayFound = index

        
        days[dayFound] = 0
        
        for bookIndex in bestSubset:
            books[bookIndex] = float('inf')
        result += len(bestSubset)
    
    output = {"optimalNumberOfBooks": result}
    
    logging.info("My result :{}".format(output))
    return jsonify(output)