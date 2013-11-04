__author__ = 'tomek'
from cats.utils.timetable import TimeTable
from itertools import groupby, combinations

class AdvancedNeighborhood(object):


    def generateChains(self, timetable, period1, period2):

        """
        Generates Kempe chain from timetable neighborhood for period1 and period2
        :param timetable:
        :param period1:
        :param period2:
        :return: dictionary, keys: Kempe chain indices, values: vertexes of chains
        """
        assignedCourses = timetable.getTimeTable()[period1] + timetable.getTimeTable()[period2]
        uniqueCourses = set(map(lambda x: x.courseId, assignedCourses))
        chains = {}
        counter = 1
        for c in assignedCourses:
            if c.courseId not in chains.keys():
                dfsStack = [c.courseId]
                while len(dfsStack)>0:
                    currentNode = dfsStack.pop()
                    chains[currentNode] = counter
                    for neighbor in timetable.neighbourhoodList[currentNode]:
                        if neighbor not in chains.keys() and neighbor in uniqueCourses:
                            dfsStack.append(neighbor)

                counter += 1
        result = {}
        for k,v in groupby(sorted(chains.iteritems(), key= lambda x: x[1]), lambda x: x[1]):
            result[k] = [a[0] for a in v]
        return result


    def generatePossibleSwappingPairs(self, timetable, chains):
        """
        Generate swapping pairs (without checking room allocation)
        :param timetable:
        :param chains: output from generateChains
        :return: pairs of indices
        """
        pairs = filter(lambda x: len(chains[x[0]])+len(chains[x[1]])>2, \
                       combinations(xrange(1,len(chains.keys())+1),2))
        return pairs

    def kempeSwap(self, timetable, period1, period2, chains):
        coursesFirst = set(timetable.getTimeTable()[period1])
        coursesSecond = set(timetable.getTimeTable()[period2])
        newCoursesFirst = set(filter(lambda x: x.courseId not in (chains[0] | chains[1]), coursesFirst)) \
                            | set(filter(lambda x: x.courseId in (chains[0] | chains[1]), coursesSecond))
        newCoursesSecond = set(filter(lambda x: x.courseId not in (chains[0] | chains[1]), coursesSecond)) \
                            | set(filter(lambda x: x.courseId in (chains[0] | chains[1]), coursesFirst))
        return (newCoursesFirst, newCoursesSecond)


    # TODO: swap structure
    # TODO: check room allocation violation
    # TODO:
