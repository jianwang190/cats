CAPACITY_PENALTY = 1
MIN_WORKINGS_DAY_PENALTY = 5
COMPACTNESS_PENALTY = 2
STABILITY_PENALTY = 1

"""Count penalty for soft constraint curriculum compactness helper function"""

def countPenaltyForCurriculumCompactness(periodsList, periodsPerDay):
    """
    Count curriculum compactness penalty for one curriculum
    @param periodsList: list with slots for curriculum (when the course of curriculum took place)
    @param periodsPerDay: periods per day in timetable
    @return:
    """
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
    return penalty

def totalSoftConstraintsForTimetable(partialTimetable, data):
    return softConstraintsPenalty(partialTimetable, data)['totalPenalty']

def softConstraintsPenalty(partialTimetable, data):
    """
    Count soft penalty for timetable
    @param partialTimetable: timetable to grade
    @param data: data for tested timetable
    @return: dictionary with penalty for : min working days, curriculum compactness, room stability and capacity, total penalty
    """
    roomCapacityPenalty = 0
    roomStabilityPenalty = 0
    minWorkingDaysPenalty = 0
    # room Set, workingDays
    information = {x.id : [set(), set()] for x in data.getAllCourses()}
    curPeriodDict = {x.id: [] for x in data.getAllCurricula()}


    for key in partialTimetable.keys():
        for cell in partialTimetable[key]:
            roomCapacityPenalty += data.getCourse(cell.courseId).studentsNum - data.getRoom(cell.roomId).capacity \
                if data.getCourse(cell.courseId).studentsNum > data.getRoom(cell.roomId).capacity else 0
            information[cell.courseId][0].add(cell.roomId)
            information[cell.courseId][1].add(key / data.periodsPerDay)
            map(lambda x: curPeriodDict[x.id].append(key), data.getCurriculumForCourseId(cell.courseId))


    curriculumCompactnessPenalty = 0
    for curriculumId in curPeriodDict.keys():
        curriculumCompactnessPenalty += countPenaltyForCurriculumCompactness(curPeriodDict[curriculumId], data.periodsPerDay)


    for key in information.keys():
        roomStabilityPenalty += len(information[key][0]) - 1 if len(information[key][0]) > 1 else 0
        minWorkingDaysPenalty += data.getCourse(key).minWorkingDays - len(information[key][1])\
            if data.getCourse(key).minWorkingDays > len(information[key][1]) else 0

    roomStabilityPenalty *= STABILITY_PENALTY
    minWorkingDaysPenalty *= MIN_WORKINGS_DAY_PENALTY
    roomCapacityPenalty *= CAPACITY_PENALTY
    curriculumCompactnessPenalty *= COMPACTNESS_PENALTY

    penalty = roomStabilityPenalty + minWorkingDaysPenalty + roomCapacityPenalty + curriculumCompactnessPenalty

    return {'penaltyMinWorkingDays': minWorkingDaysPenalty, 'penaltyRoomStability': roomStabilityPenalty,\
            'penaltyRoomCapacity': roomCapacityPenalty,'penaltyCurriculumCompactness': curriculumCompactnessPenalty,\
            'totalPenalty' : penalty}

