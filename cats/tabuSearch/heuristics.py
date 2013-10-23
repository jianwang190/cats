from cats.utils.timetable import TimeTableFactory, CellOfTimeTable
import math


def costFunctionStage1(partialTimetable, data, courseId):
    apd =  partialTimetable.availablePeriodsRooms(data.constraints, courseId)["availablePeriodsNum"]
    cx = map(lambda x: x.id, data.courses).index(courseId)
    nl = data.courses[cx].lectureNum - len(partialTimetable.assignedLectures(courseId))

    return float(apd)/math.sqrt(nl)

def costFunctionStage2(partialTimetable, data, courseId):
    aps = partialTimetable.availablePeriodsRooms(data.constraints, courseId)
    cx = map(lambda x: x.id, data.courses).index(courseId)
    nl = data.courses[cx].lectureNum - len(partialTimetable.assignedLectures(courseId))
    return float(aps["availablePairsNum"])/math.sqrt(nl)




"""TODO: write unittests"""

def getNextCourse(partialTimetable, data):

    courses = sorted([(x, costFunctionStage1(partialTimetable, data, x.id)) \
            for x in data.courses], \
            key=lambda x: x[1], \
            reverse=True)

    selectedStage1 = filter(lambda x: x[1]==courses[0][1], courses)


    if len(selectedStage1)>1:
        selectedStage2 = sorted( \
            map(lambda x: (x[0], costFunctionStage2(partialTimetable, data, x[0].id)), selectedStage1), key=lambda x: x[1], reverse=True)
        selectedStage2 = map(lambda x: x[0], filter(lambda x: x[1]==selectedStage2[0][1], selectedStage2))
        if len(selectedStage2)>1:
            return sorted(selectedStage2, key=lambda x: partialTimetable.conflictingCourses(x.id))[0]
        else:
            return selectedStage2[0]
    else:
        return selectedStage1[0]

"""TODO: Test the function, not checked if working properly, ADD curriculumCompactness, RoomStability"""
def softConstraints(partialTimetable, data, courseId, period, roomId, curId):

    partialTimetable[period].append(CellOfTimeTable(courseId, roomId, curId))

    penalty = 0
    dataCourse = [c for c in data.courses if (c.id == courseId)]
    roomCapacity = ([r.capacity for r in data.rooms if (r.id == roomId)])

    if(dataCourse.studentsNum > roomCapacity):
        penalty += roomCapacity - dataCourse.studentsNum

    workingDaysSet = set()
    totalNumberLectures = 0;
    for key in partialTimetable.keys():
        for cell in partialTimetable[key]:
            if(cell.courseId == courseId and cell.curId == curId):
                ++totalNumberLectures
                workingDaysSet.add(key / data.periodsPerDay)
    daysNum = totalNumberLectures - len(workingDaysSet)
    workingDaysNumPartial = dataCourse.lectureNum - totalNumberLectures + daysNum
    if(workingDaysNumPartial < dataCourse.minWorkingDays):
        penalty += 5 * (dataCourse.minWorkingDays - workingDaysNumPartial)

    return penalty

