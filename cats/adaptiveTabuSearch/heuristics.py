from cats.utils.timetable import TimeTableFactory
from softConstraints2 import totalSoftConstraintsForTimetable
from itertools import groupby
import math


UAC_CONST = 1.0
SOFT_CONST = 0.5


def initialSolution(timetable, data):


    while len(data.getUnfinishedCourses())>0:

        nextCourse = getNextCourse(timetable, data)
        if feasibleInsertion(timetable, nextCourse.id, data)==False:
            break
    print


    #print "##### INITIAL SOLUTION FINISHED #####"
    #print ">>> UNASSIGNED COURSES:\n\tid\tlectureNum\tassigned"
    #for c in data.getUnfinishedCourses():
    #    print "\t", "\t".join([c.id, str(c.lectureNum), " ", str(c.assignedLectureNum), \
    #                           " ".join(timetable.neighbourhoodList[c.id])])

""" Dla Filipa """
def initialSolutionWithReturn(timetable, data):
    while len(data.getUnfinishedCourses())>0:
        nextCourse = getNextCourse(timetable, data)
        if feasibleInsertion(timetable, nextCourse.id, data)==False:
            break

    return timetable


def feasibleInsertion(partialTimeTable, courseId, data):

    """
    do the feasible insertion of lecture of course to period and room
    :param partialTimeTable:
    :param courseId:
    :param data:
    :return: False, if no insertion can be made
    """
    availablePairs = []

    periods = partialTimeTable.availablePeriodsRooms(data.getAllConstraints(), courseId)["availablePeriods"]
    for p in periods:
        for r in partialTimeTable.availableRoomsList(p, data):
            availablePairs.append((p,r))

    solutionRankings = \
        map(lambda x: (UAC_CONST*partialTimeTable.unavailableUnfinishedCoursesLectureNum(x[0], courseId, data) \
            + SOFT_CONST*totalSoftConstraintsForTimetable(partialTimeTable.getTimeTable(), data), x), \
            availablePairs)

    solutionRankings.sort(key = lambda x: x[0])
    if len(solutionRankings)>0:
        period = solutionRankings[0][1][0]
        room = solutionRankings[0][1][1]

        # assign matching course-room to period
        partialTimeTable.getTimeTable()[period].append((courseId, room))
        # update course assigned lecture number
        data.popCourse(courseId)
    else:
        return False




def costFunctionStage1(partialTimetable, data, courseId):
    apd = partialTimetable.availablePeriodsRooms(data.getAllConstraints(), courseId)["availablePeriodsNum"]
    nl = data.getCourse(courseId).lectureNum - data.getCourse(courseId).assignedLectureNum

    return float(apd) / math.sqrt(nl)


def costFunctionStage2(partialTimetable, data, courseId):
    aps = partialTimetable.availablePeriodsRooms(data.getAllConstraints(), courseId)
    nl = data.getCourse(courseId).lectureNum - data.getCourse(courseId).assignedLectureNum

    return float(aps["availablePairsNum"])/math.sqrt(nl)





def getNextCourse(partialTimetable, data):
    courses = sorted([(x, costFunctionStage1(partialTimetable, data, x.id)) \
                      for x in data.getUnfinishedCourses()], \
                     key=lambda x: x[1])

    selectedStage1 = filter(lambda x: x[1] == courses[0][1], courses)

    if len(selectedStage1) > 1:
        selectedStage2 = sorted( \
            map(lambda x: (x[0], costFunctionStage2(partialTimetable, data, x[0].id)), selectedStage1),
            key=lambda x: x[1])
        selectedStage2 = map(lambda x: x[0], filter(lambda x: x[1] == selectedStage2[0][1], selectedStage2))
        if len(selectedStage2) > 1:
            #print "DRAW",
            return sorted(selectedStage2, key=lambda x: partialTimetable.conflictingCourses(x.id))[0]
        else:
            #print "STAGE2",
            return selectedStage2[0]
    else:
        #print "STAGE1", [(c[0].id, round(c[1],2)) for c in courses[:4]],
        return selectedStage1[0][0]


