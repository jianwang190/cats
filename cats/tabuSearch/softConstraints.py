from cats.utils.timetable import TimeTableFactory, CellOfTimeTable


CAPACITY_PENALTY = 1
MIN_WORKINGS_DAY_PENALTY = 5
COMPACTNESS_PENALTY = 2
STABILITY_PENALTY = 1

"""Count total penalty for soft constraints"""
def totalSoftConstraintsPenalty(partialTimetable, data, courseId, curriculumId):
    penalty = 0
    result = softConstraintsPenalty(partialTimetable, data, courseId, curriculumId)
    penalty += result['penaltyMinWorkingDays'] + result['penaltyCurriculumCompactness'] + result['penaltyRoomStability'] + result['penaltyRoomCapacity']
    return penalty



"""Count soft penalty for room capacity for course (roomIdList)"""
def penaltyRoomCapacity(data, courseId, roomIdList):
    penalty = 0

    dataCourse = ([c for c in data.courses if (c.id == courseId)])[0]
    roomCapacityList = []
    for roomId in roomIdList:
        for r in data.rooms:
            if roomId == r.id:
                roomCapacityList.append(r.capacity)

    for roomCap in roomCapacityList:
        if dataCourse.studentsNum > roomCap:
            penalty += dataCourse.studentsNum - roomCap

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

"""Count soft penalty for minimum working days and room stability and curriculum compactness"""
def softConstraintsPenalty(partialTimetable, data, courseId, curriculumId = None):
    penaltyMinWorking = 0
    penaltyRoomStability = 0
    workingDaysSet = set()
    roomIdSet = set()
    roomIdList = []
    curriculumPeriodsList = []
    totalNumberLectures = 0

    dataCourse = ([c for c in data.courses if (c.id == courseId)])[0]

    for key in partialTimetable.keys():
        for cell in partialTimetable[key]:
            if cell.courseId == courseId:
                totalNumberLectures += 1
                workingDaysSet.add(key / data.periodsPerDay)
                roomIdSet.add(cell.roomId)
                roomIdList.append(cell.roomId)
            if curriculumId in cell.curriculumId:
                    curriculumPeriodsList.append(key)
    """Room capacity penalty for one course and rooms list"""
    roomCapacityPenalty = penaltyRoomCapacity(data, courseId, roomIdList)

    """Minimum working days penalty"""
    workingDaysNumPartial = dataCourse.lectureNum - totalNumberLectures + len(workingDaysSet)
    if workingDaysNumPartial < dataCourse.minWorkingDays:
        penaltyMinWorking += MIN_WORKINGS_DAY_PENALTY * (dataCourse.minWorkingDays - workingDaysNumPartial)

    """Room stability penalty"""
    if len(roomIdSet) > 1:
        penaltyRoomStability += STABILITY_PENALTY * (len(roomIdSet) - 1)

    """Curriculum compactness penalty"""
    penaltyCurriculumCompactness = countPenaltyForCurriculumCompactness(curriculumPeriodsList, data.periodsPerDay)

    return {'penaltyMinWorkingDays': penaltyMinWorking, 'penaltyRoomStability': penaltyRoomStability,
            'penaltyCurriculumCompactness': penaltyCurriculumCompactness, 'penaltyRoomCapacity': roomCapacityPenalty}