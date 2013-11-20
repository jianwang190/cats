import random
from cats.adaptiveTabuSearch.softConstraints2 import softConstraintsPenalty, totalSoftConstraintsForTimetable
from cats.adaptiveTabuSearch.basicNeighborhood import BasicNeighborhood
from cats.adaptiveTabuSearch.advancedNeighborhood import AdvancedNeighborhood
from operator import itemgetter
from cats.adaptiveTabuSearch import tabuSearch
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


def checkIfAllDone(selectedLecturesDict):
    for x in selectedLecturesDict.keys():
        if selectedLecturesDict[x] == 0:
            return False
    return True

def getFirstUndone(selectedLecturesDict):
    for x in selectedLecturesDict.keys():
        if selectedLecturesDict[x] == 0:
            return x


def produceRandomlySimpleOrKempeSwap(timetable, data, n, q):
    """
    n feasible moves of SimpleSwap or KempeSwap are randomly and sequentially produces each
     involving at least one of selected n lectures
    :param selectedLectures: list of selected lectures to swa
    """
    initialSolution = timetable.copy()
    selectedLectures = rankingOfLectures(initialSolution.getTimeTable(), data, n, q)
    print "INITIAL PENALTY", totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)

    # 0 denote that was no move with this lecture
    selectedLecturesDict = {x: 0 for x in selectedLectures}
    b = BasicNeighborhood()
    a = AdvancedNeighborhood()

    while checkIfAllDone(selectedLecturesDict) == False:
        choice = random.choice(['kempeSwap', 'simpleSwap'])
        lecture = getFirstUndone(selectedLecturesDict)

        if choice == 'simpleSwap':
            b.clearBasicList()
            b.simpleSwap(initialSolution.getTimeTable(), initialSolution.neighbourhoodList, len(data.getAllRooms()))
            possibleSwaps = filter(lambda swap: (swap[0].courseId == lecture[0] and swap[0].period == lecture[2])\
                or (swap[1].courseId == lecture[0] and swap[1].period == lecture[2]), b.getBasicList())


            if len(possibleSwaps) > 0:
                selectedSwap = random.choice(possibleSwaps)
                print selectedSwap
                initialSolution.timeTable = tabuSearch.doSimpleSwap(initialSolution.getTimeTable(), selectedSwap)
                selectedLecturesDict[lecture] = 1
            print "SIMPLE", totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)
        else:
            neighborhood = a.exploreNeighborhood(initialSolution, data)
            neighborhood = filter(lambda x: x[0][0]==lecture[1] or x[0][1]==lecture[1] , neighborhood)
            neighborhood = filter(lambda x: lecture[0] in x[1]["moves"][0][1] or lecture[0] in x[1]["moves"][1][1], neighborhood)
            for i in neighborhood:
                print i
            print "KEMPE"

    print "AFTER SIMPLE RANDOM SWAP", totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)



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
