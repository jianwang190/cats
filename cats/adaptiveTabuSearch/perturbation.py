import random
from cats.adaptiveTabuSearch.softConstraints2 import softConstraintsPenalty
from operator import itemgetter
"""Perturbation"""
PERTURBATION_STRENGTH_MIN = 4
PERTURBATION_STRENGTH_MAX = 15
DISTRIBUTION_PARAMETER = -4


def rankingOfLectures(partialTimetable, data, n, q):
    """
    Function to identify a set of the first q highly-penalized lectures and select n lectures from them,
    the lecture of rank k is selected with probability distribution, n <= q
    :param partialTimetable: timetable
    :param data: information about data
    :param n: number of selected lectures from first q highly penalized ones
    :param q:
    """
    # dictionary containing soft penalties for each of lecture assigned to timetable (courseId, roomId, slot) : penalty
    perturbationDict = softConstraintsPenalty(partialTimetable, data, "perturbation")['perturbationPenalty']
    #perturbation penalty in form courseId, roomId, slot
    rankingLectures = sorted(perturbationDict.items(), key=itemgetter(1), reverse=True)
    listItems = map(lambda x: x[0], rankingLectures[:q])
    selectedLectures = selectRandom(listItems, n)
    return selectedLectures

"""TODO: write envoking moves"""
def produceRandomlySimpleOrKempeSwap(selectedLectures):
     """
     n feasible moves of SimpleSwap or KempeSwap are randomly and sequentially produces each
     invloving at least one of selected n lectures
    :param selectedLectures: list of selected lectures to swap
    """
     choice = random.choice(['kempeSwap', 'simpleSwap'])
     # check if lecture is not in tabu list and run simpleSwap or kempeSwap


def selectRandom(listItems, numberOfSelectedItems):

    """
    random selection of elements in list with following distribution for elements :
    P(k) ~ k (DISTRIBUTION_PARAMETER), where k is number of lecture in rank
    :param listItems: list of tuples
    :param numberOfSelectedItems: number of selected unique tuples from listItems
    :return: list with tuples of selected items
    """
    selectedValues = []
    probabilities = map(lambda x : float(x**(DISTRIBUTION_PARAMETER)), range(1, len(listItems) + 1))

    while len(selectedValues) < numberOfSelectedItems:
        x = random.uniform(0, 1)
        cumulativeProbability = 0.0
        for item, itemProbability in zip(listItems, probabilities):
            cumulativeProbability += itemProbability
            if x < cumulativeProbability:
                break
        selectedValues.append(item)
        index = listItems.index(item)
        listItems.remove(item)
        probabilities.pop(index)
    return selectedValues
