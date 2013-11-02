from cats.utils.timetable import TimeTableFactory, CellOfTimeTable
from softConstraints import totalSoftConstraintsPenalty
from itertools import groupby
import math


UAC_CONST = 1.0
SOFT_CONST = 0.5


def initialSolution(timetable, data):


    while len(data.getUnfinishedCourses())>0:

        nextCourse = getNextCourse(timetable, data)
        #for k in timetable.getTimeTable():
        #    print k, [(x.courseId, x.roomId) for x in timetable.getTimeTable()[k]]
        #print nextCourse.id,
        if feasibleInsertion(timetable, nextCourse.id, data)==False:
            break
    print


    #print ">>> TIMETABLE"
    #for k in timetable.getTimeTable():
    #    print k, [(x.courseId, x.roomId) for x in timetable.getTimeTable()[k]]

    #print ">>> CONSTRAINTS"
    #l = sorted(data.getAllConstraints(), key = lambda x: x.id)
    #for c, cl in groupby(l, key=lambda x: x.id):
    #    print c, [timetable.getKey(ce.day, ce.dayPeriod) for ce in cl]

    print "##### INITIAL SOLUTION FINISHED #####"
    print ">>> UNASSIGNED COURSES:\n\tid\tlectureNum\tassigned"
    for c in data.getUnfinishedCourses():
        print "\t", "\t".join([c.id, str(c.lectureNum), " ", str(c.assignedLectureNum), \
                               " ".join(timetable.neighbourhoodList[c.id])])



""" do the feasible insertion of lecture of course to period and room """
def feasibleInsertion(partialTimeTable, courseId, data):

    availablePairs = []

    periods = partialTimeTable.availablePeriodsRooms(data.getAllConstraints(), courseId)["availablePeriods"]
    for p in periods:
        for r in partialTimeTable.availableRoomsList(p, data):
            availablePairs.append((p,r))

    solutionRankings = \
        map(lambda x: (UAC_CONST*partialTimeTable.unavailableUnfinishedCoursesLectureNum(x[0], courseId, data) \
            + SOFT_CONST*totalSoftConstraintsPenalty(partialTimeTable.getTimeTable(), data, courseId), x), \
            availablePairs)

    solutionRankings.sort(key = lambda x: x[0])
    if len(solutionRankings)>0:
        period = solutionRankings[0][1][0]
        room = solutionRankings[0][1][1]
        #print solutionRankings[0][0]
        # assign matching course-room to period
        partialTimeTable.getTimeTable()[period].append(
            CellOfTimeTable(courseId, room))
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


"""TODO: write unittests"""


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



