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
        uniqueCourses = set(map(lambda x: x[0], assignedCourses))
        chains = {}
        counter = 1
        for c in assignedCourses:
            if c[0] not in chains.keys():
                dfsStack = [c[0]]
                while len(dfsStack)>0:
                    currentNode = dfsStack.pop()
                    chains[currentNode] = counter
                    for neighbor in timetable.neighbourhoodList[currentNode]:
                        if neighbor not in chains.keys() and neighbor in uniqueCourses:
                            dfsStack.append(neighbor)

                counter += 1
        result = {}
        for k,v in groupby(sorted(chains.iteritems(), key= lambda x: x[1]), lambda x: x[1]):
            result[k] =set([a[0] for a in v])
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

    def exploreNeighborhood(self, timetable, data):
        result = []
        for pair in combinations(range(0, len(timetable.getTimeTable())),2):

            chains = self.generateChains(timetable, pair[0], pair[1])
            swappingPairs = self.generatePossibleSwappingPairs(timetable, chains)

            # double chains
            for swap in swappingPairs:
                result.append( \
                    (pair, \
                     self.kempeSwap(timetable, pair[0], pair[1], (chains[swap[0]], chains[swap[1]]))))
            #single chains
            for c in chains.itervalues():
                result.append(\
                    (pair, self.kempeSwap(timetable, pair[0], pair[1], (c, set([]))))
                    )

        # room allocation violation

        
        result = filter(lambda x: len(x[1]["newPeriods"][0])<=len(data.rooms) and len(x[1]["newPeriods"][1])<=len(data.rooms), result)

        return result






    def kempeSwap(self, timetable, period1, period2, chains):
        """
        Perform Kempe swap on 2 chains
        :param timetable:
        :param period1:
        :param period2:
        :param chains: pair of chains, chain: list of indices
        :return: pair of sets containing courses for period1 and period2
        """
        coursesFirst = set(timetable.getTimeTable()[period1])
        coursesSecond = set(timetable.getTimeTable()[period2])
        newCoursesFirst = set(filter(lambda x: x[0] not in (chains[0] | chains[1]), coursesFirst)) \
                            | set(filter(lambda x: x[0] in (chains[0] | chains[1]), coursesSecond))
        newCoursesSecond = set(filter(lambda x: x[0] not in (chains[0] | chains[1]), coursesSecond)) \
                            | set(filter(lambda x: x[0] in (chains[0] | chains[1]), coursesFirst))

        return { "newPeriods": (newCoursesFirst, newCoursesSecond), \
                "moves": ((period1, (coursesFirst - newCoursesFirst)), (period2, (coursesSecond-newCoursesSecond)))}




def doKempeSwap(((period1, period2), swap), timetable):
    newTimetable = {x: timetable[x][:] for x in timetable.keys()}
    newTimetable[period1] = [x for x in swap["newPeriods"][0]]
    newTimetable[period2] = [x for x in swap["newPeriods"][1]]
    return newTimetable