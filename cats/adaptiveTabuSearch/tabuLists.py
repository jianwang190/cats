# separate object of TabuList class should be created for N1 and N2
from cats.adaptiveTabuSearch import softConstraints2


class Move(object):
    def __init__(self, period, roomId, iteration):
        self.period = period
        self.room = roomId
        self.iteration = iteration


class AdvancedMove(object):
    def __init__(self, period, iteration):
        self.period = period
        self.iteration = iteration

class GenericTabuList(object):

    def tabuTenure(self, courseId, partialTimetable, data):
        """Tabu tenure of courseId is tuned adaptively according to the current solution quality f and moving frequency

        :param courseId:
        :param partialTimetable:
        :param data:
        """
        #Moving frequency of lectures of courseId

        movingFreqCourse = len(self.tabuList[courseId])
        f = softConstraints2.totalSoftConstraintsForTimetable(partialTimetable, data)
        tt =  f + self.parameter[courseId][0] * movingFreqCourse
        return tt
    def coefficientTabuTenure(self, courseList, neighborhoodList):
        """
        Function to count coefficient for tabu tenure (number of conflicting courses / total number of courses)
        :param courseList: list of course ids
        :param neighborhoodList:neighborhood list for courses
        :return: dictionary with coefficient for each courseId
        """
        totalNumberOfCourses = len(courseList)
        parameter = {x.id : [] for x in courseList}

        map(lambda x : parameter[x].append(float(len(neighborhoodList[x])) / float(totalNumberOfCourses)), neighborhoodList)
        return parameter


class TabuList(GenericTabuList):
    """"
    Contains tabu moves in tabuList
    """
    def __init__(self, courseList, neighborhoodList):
        self.tabuList = {x.id : [] for x in courseList}
        self.parameter = self.coefficientTabuTenure(courseList, neighborhoodList)


    def addTabuMove(self, courseId, period, roomId, iteration):
        """
        Add tabu move
        :param courseId:
        :param period:
        :param roomId:
        :param iteration:
        :return:
        """
        move = Move(period, roomId, iteration)
        self.tabuList[courseId].append(move)





    def isTabuMove(self, courseId, period, roomId, currentIteration, tt):
        """
        Check if move is on tabuList
        :param courseId:
        :param period:
        :param roomId:
        :param currentIteration:
        :param tt: tabu tenure
        :return:
        """
        return len( \
            filter(lambda x: x.period==period and x.room==roomId and x.iteration+tt>=currentIteration, self.tabuList[courseId]))>0




class AdvancedTabuList(GenericTabuList):
    """
    Tabu list for advanced neighbourhood
    """
    def __init__(self, courseList, neighborhoodList):
        self.tabuList = {x.id: [] for x in courseList}
        self.parameter = self.coefficientTabuTenure(courseList, neighborhoodList)


    def addTabuMoves(self, ((period1, moves1), (period2, moves2))):
        """
        Add tabu moves
        :return:
        """
        for (courseId, _) in moves1:
            self.addTabuMove(courseId, period1)
        for (courseId, _) in moves2:
            self.addTabuMove((courseId, period2))

    def addTabuMove(self, courseId, period, iteration):
        """
        Add tabu move
        :param courseId:
        :param period:
        :param iteration:
        :return:
        """
        self.tabuList[courseId].append(AdvancedMove(period, iteration))

    def isTabuMove(self, courseId, period, currentIteration, tt):
        """
        Check if element is tabu move
        :param courseId:
        :param period:
        :param currentIteration:
        :param tt:
        :return:
        """
        return len(\
            filter(lambda x: x.period==period and x.iteration+tt>=currentIteration, self.tabuList[courseId]))>0