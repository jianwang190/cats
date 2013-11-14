import random
from cats.adaptiveTabuSearch.softConstraints2 import softConstraintsPenalty
from operator import itemgetter
"""Perturbation"""
PERTURBATION_STRENGTH_MIN = 4
PERTURBATION_STRENGTH_MAX = 15

"""n - number of selected lectures form the first q highly penalized ones"""
def rankingOfLectures(partialTimetable, data, n, q):
    perturbationDict = softConstraintsPenalty(partialTimetable, data, "perturbation")
    rankingLectures = sorted(perturbationDict.items(), key=itemgetter(1), reverse=True)

    pass

def selectRandom(listItems, numberOfSelectedItems):

    """

    :param listItems: list of tuples
    :param numberOfSelectedItems: number of selected unique tuples from listItems
    :return: list with tuples of selected items
    """
    selectedValues = []
    probabilities = map(lambda x : float(x**(-4)), range(1, len(listItems) + 1))

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
