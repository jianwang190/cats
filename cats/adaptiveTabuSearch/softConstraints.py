from cats.utils.timetable import TimeTableFactory, CellOfTimeTable


CAPACITY_PENALTY = 1
MIN_WORKINGS_DAY_PENALTY = 5
COMPACTNESS_PENALTY = 2
STABILITY_PENALTY = 1

"""Count total penalty for soft constraints for whole solution (timetable)"""
def totalSoftConstraintsForTimetable(partialTimetable, data):

    totalPenalty = softConstraintsPenalty(partialTimetable, data)['partialTotalPenalty']
    totalPenalty += curriculumCompactnessPenalty(partialTimetable, data)

    return totalPenalty



"""Count soft penalty for room capacity for course (roomIdList)"""
def penaltyRoomCapacity(data, courseId, roomIdList):

    dataCourse = data.getCourse(courseId)
    penalty = sum(filter(lambda x: x > 0, map(lambda x: dataCourse.studentsNum - data.getRoom(x).capacity, roomIdList)))
    penalty = CAPACITY_PENALTY * penalty
    return penalty



"""Count penalty for soft constraint curriculum compactness helper function"""

def countPenaltyForCurriculumCompactness(periodsList, periodsPerDay):
    penalty = 0
    for i in range(0, len(periodsList)):
        if i > 0 and periodsList[i - 1] + 1 == periodsList[i] and (periodsList[i - 1] / periodsPerDay == periodsList[i] / periodsPerDay):
            beforeLecture = True
        else:
            beforeLecture = False
        if i < len(periodsList) - 1 and (periodsList[i + 1] - 1 == periodsList[i]) and (periodsList[i + 1] / periodsPerDay == periodsList[i] / periodsPerDay):
            afterLecture = True
        else:
            afterLecture = False
        if beforeLecture is False and afterLecture is False:
            penalty += 1
    penalty = COMPACTNESS_PENALTY * penalty
    return penalty


"""Count penalty for curriculum compactness for all curriculums"""
def curriculumCompactnessPenalty(partialTimetable, data):

    curPeriodDict = {x.id: [] for x in data.getAllCurricula()}

    for cur in curPeriodDict.keys():
        for key in partialTimetable.keys():
            for cell in partialTimetable[key]:
                if cell.courseId in data.getCurriculum(cur).members:
                    curPeriodDict[cur].append(key)

    penaltyCurriculumCompactness = 0
    for curriculumId in curPeriodDict.keys():
        penaltyCurriculumCompactness += countPenaltyForCurriculumCompactness(curPeriodDict[curriculumId], data.periodsPerDay)

    return penaltyCurriculumCompactness


"""Count soft penalty for minimum working days and room stability and curriculum compactness"""


def softConstraintsPenalty(partialTimetable, data):

    penaltyMinWorking = 0
    penaltyRoomStability = 0
    #totalNumberOfLextures , Set od days
    workingDaysDict = {x.id :[0, set()] for x in data.getAllCourses()}
    roomIdDict = {x.id: [] for x in data.getAllCourses()}


    for key in partialTimetable.keys():
        for cell in partialTimetable[key]:
            workingDaysDict[cell.courseId][1].add(key / data.periodsPerDay)
            workingDaysDict[cell.courseId][0] += 1
            roomIdDict[cell.courseId].append(cell.roomId)

    """Room capacity penalty for one course and rooms list"""
    roomCapacityPenalty = 0
    for key in roomIdDict.keys():
        roomCapacityPenalty += penaltyRoomCapacity(data, key, roomIdDict[key])

    """Minimum working days penalty"""
    for key in workingDaysDict.keys():
        workingDaysNumPartial = data.getCourse(key).lectureNum - workingDaysDict[key][0] + len(workingDaysDict[key][1])
        if workingDaysNumPartial < data.getCourse(key).minWorkingDays:
            penaltyMinWorking += MIN_WORKINGS_DAY_PENALTY * (data.getCourse(key).minWorkingDays - workingDaysNumPartial)

    """Room stability penalty"""
    for key in roomIdDict.keys():
        if len(set(roomIdDict[key])) > 1:
            penaltyRoomStability += STABILITY_PENALTY * (len(set(roomIdDict[key])) - 1)

    partialtotalPenalty = penaltyMinWorking + penaltyRoomStability + roomCapacityPenalty

    return {'penaltyMinWorkingDays': penaltyMinWorking, 'penaltyRoomStability': penaltyRoomStability,
             'penaltyRoomCapacity': roomCapacityPenalty, 'partialTotalPenalty' : partialtotalPenalty}
