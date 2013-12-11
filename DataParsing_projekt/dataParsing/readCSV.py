from dataParsing.inputDataStructure import Course, Room, Curriculum, Constraint
from dataParsing.data import DictData
from itertools import groupby
import operator



class DataParser(object):

    def __init__(self):
        self.data = DictData()
        self.buffer = []

    def translateData(self):
        """
        Create unique ids for teachers
        Create output file with unique ids

        """
        path = "/home/kasia/PycharmProjects/DataParsing/DataSchool/zest_zarz_planem.csv"
        pathOutputFile = "/home/kasia/PycharmProjects/DataParsing/OutputDataSchool/zest_zarz_planem.csv"
        outputFile= open(pathOutputFile, 'w')
        index = 0

        f = open(path, "r")
        content = map(lambda x: x.rstrip('\n').strip().split(';'), f.readlines())
        content = content[1:]
        for row in content:
            NameSurname = str(row[13]).split(' ')
            teacherId = NameSurname[0][:1] + NameSurname[0][-1:]+NameSurname[1][:1] + NameSurname[1][-1:]
            row = row[:-1]
            row.append(teacherId)
            outputRow = ';'.join([str(elem) for elem in row])
            outputFile.write(outputRow + '\n')

    def translateGroupsOfStudents(self):
        """
        Update file grupy_uczniow with unique teachers ids
        Create output file

        """
        path = "/home/kasia/PycharmProjects/DataParsing/DataSchool/zest_grupy_uczniow.csv"
        pathOutputFile = "/home/kasia/PycharmProjects/DataParsing/OutputDataSchool/zest_grupy_uczniow.csv"
        outputFile= open(pathOutputFile, 'w')
        index = 0

        f = open(path, "r")
        content = map(lambda x: x.rstrip('\n').strip().split(';'), f.readlines())
        content = content[1:]
        for row in content:
            NameSurname = str(row[4]).split(' ')
            teacherId = NameSurname[0][:1] + NameSurname[0][-1:]+NameSurname[1][:1] + NameSurname[1][-1:]
            row2 = row[:3]
            row2.append(teacherId)
            for i in row[5:]:
                row2.append(i)
            outputRow = ';'.join([str(elem) for elem in row2])
            outputFile.write(outputRow + '\n')


    def readRooms(self):
        """
        Read rooms from file, getting essential information (name of room, capacity, type)

        """
        path = "/home/kasia/PycharmProjects/DataParsing/DataSchool/zest_slownik_miejsc_zajec2.csv"
        index = 0
        f = open(path, "r")
        content = map(lambda x: x.rstrip('\n').strip().split(';'), f.readlines())
        content = content[1:]
        for row in content:
            roomId = row[1]
            type = row[3]
            capacity = int(row[4])
            room = Room(roomId, capacity, type)
            self.data.rooms[roomId] = room

    def readCurriculumClasses(self):
        """
        Read groups and classes from file grupy uczniow, add groups to appropriate classes

        """
        path = "/home/kasia/PycharmProjects/DataParsing/DataSchool/zest_grupy_uczniow.csv"
        index = 0
        with open(path, 'rb') as f:
            for line in f:
                index += 1
                buffer = line.strip().split(';')
                if index > 1:
                    grupaNadrzedna = str(buffer[1])
                    nazwaGrupy = str(buffer[2])
                    liczbaUczniow = int(buffer[5]) if len(buffer[5]) > 0 else 0

                    if grupaNadrzedna == ' ':
                        self.data.curricula[nazwaGrupy] = Curriculum(nazwaGrupy, liczbaUczniow)
                    else:
                        self.data.courses[nazwaGrupy] = Course(nazwaGrupy, '', 0,  0, liczbaUczniow)
                        lista = self.data.getMembersCurriculum(grupaNadrzedna)
                        lista.append(nazwaGrupy)
                        self.data.curricula[grupaNadrzedna].members = lista


    def checkIfNotExist(self, groupsBetweenClasses, groupedSet):
        """
        Check if group exists in dictionary containing groups between classes

        :param groupsBetweenClasses: dictionary with groups between classes
        :param groupedSet:set containing groups
        :return: True or False

        """
        for key in groupsBetweenClasses.keys():
            if groupedSet == groupsBetweenClasses[key]:
                return True
        return False


    def combineIntoGroups(self):
        """
        read Classes and groups
        isolate groups between classes, add courses to curriculum, count number of lessons, number of students attending courses
        add names of teacher

        """
        self.readCurriculumClasses()

        path = "/home/kasia/PycharmProjects/DataParsing/OutputDataSchool/zest_zarz_planem.csv"
        groupsBetweenClasses = {}

        # value in groupsBetweenClassesInfo tuple :(number of students, number of lectures, teacher name)
        groupsBetweenClassesInfo = {}
        f = open(path, "r")
        content = map(lambda x: x.rstrip('\n').strip().split(';'), f.readlines())
        content = content[1:]

        #groups lessons: name of subject, start time, end time, day and teacher id
        sortedContent = sorted(content, key=operator.itemgetter(7, 8, 9, 10, 11, 13))
        index = 0
        for key, group in groupby(sortedContent, key=operator.itemgetter(7, 8, 9, 10, 11, 13)):
            groupedList = list(group)
            if len(groupedList) > 1:
                index += 1
                groupedSet = set(map(lambda x: (x[2], x[11]), groupedList))
                name = groupedList[0][11]
                groupName = groupedList[0][2]
                wholeName = groupName + "_" + name
                if len(groupedSet) > 1 and self.checkIfNotExist(groupsBetweenClasses, groupedSet) == False:
                    groupsBetweenClasses[wholeName] = groupedSet
                    groupsBetweenClassesInfo[wholeName] = (0, 1, groupedList[0][13])
                elif len(groupedSet) > 1 and self.checkIfNotExist(groupsBetweenClasses, groupedSet) == True:
                    numberLecture = groupsBetweenClassesInfo[wholeName][1] + 1 #one lecture
                    teacherName = groupsBetweenClassesInfo[wholeName][2]
                    groupsBetweenClassesInfo[wholeName] = (0, numberLecture, teacherName)

        #group by id of group, name of subject (count number of lessons in group and the name of teacher)
        sortedContent = sorted(content, key=operator.itemgetter(2, 11))
        for key, group in groupby(sortedContent, key=operator.itemgetter(2, 11)):
            groupedList = list(group)

            # name of group appear as name of class
            coursesToAdd = filter(lambda x: x[2] in self.data.curricula.keys(), groupedList)
            if len(coursesToAdd) > 0:
                nameOfSubject = coursesToAdd[0][2] + "_" + coursesToAdd[0][11]
                self.data.courses[nameOfSubject] = Course(nameOfSubject, coursesToAdd[0][13], len(groupedList),0, \
                                                    self.data.curricula[coursesToAdd[0][2]].studentsNumber)
                curriculum = groupedList[0][2]
                lista = self.data.getMembersCurriculum(curriculum)
                lista.append(nameOfSubject)
                self.data.curricula[curriculum].members = lista
            elif groupedList[0][2] not in groupsBetweenClasses:
                course = self.data.getCourse(groupedList[0][2])
                course.lectureNum = len(groupedList)
                course.teacher = groupedList[0][13]
                course.nameOfSubject = groupedList[0][11]
                self.data.courses[groupedList[0][2]] = course


        #  count number of students, add new courses between classes
        for helperGroup in groupsBetweenClasses.keys():
            totalNumberOfStudents = 0
            for group in groupsBetweenClasses[helperGroup]:
                for course in self.data.courses.keys():
                    if group[0] == course:
                        totalNumberOfStudents += self.data.courses[course].studentsNum
            tuple = groupsBetweenClassesInfo[helperGroup]
            groupsBetweenClassesInfo[helperGroup] = (totalNumberOfStudents, tuple[1], tuple[2])
            #add new courses
            lectureNumber = groupsBetweenClassesInfo[helperGroup][1]
            self.data.courses[helperGroup] = Course(helperGroup, groupsBetweenClassesInfo[helperGroup][2], lectureNumber,  0, \
                                                    groupsBetweenClassesInfo[helperGroup][0])



        #remove unimportant courses, which are in connections between classes
        for helperGroup in groupsBetweenClasses.keys():
            lista = filter(lambda x: x[0] in self.data.courses.keys(), groupsBetweenClasses[helperGroup])
            for x in lista:
                del self.data.courses[x[0]]

        # replace old names with new ones (those courses appearing between classes)
        for key in self.data.curricula.keys():
            lista = self.data.getMembersCurriculum(key)
            for i in range(0, len(lista)):
                for helperGroup in groupsBetweenClasses.keys():
                    for courseName in groupsBetweenClasses[helperGroup]:
                        if courseName[0] == lista[i]:
                            lista[i] = helperGroup

    def writeAllCourses(self):
        """
        write courses to file in following format
        SubjectName, teacherId, number of lectures, minimum Days Working,number of students, type of Class

        """
        pathOutputFile = "/home/kasia/PycharmProjects/DataParsing/OutputDataSchool/courses2.csv"
        outputFile= open(pathOutputFile, 'w')


        for x in self.data.courses.keys():
            course = self.data.courses[x]

            if course.teacher == ''.encode('cp1250'):
                course.teacher = 'None'
            if course.teacher != 'None' and course.lectureNum != 0 and course.studentsNum != 0:
                outputRow =  course.id + ' ' + course.teacher + ' ' + str(course.lectureNum) + ' ' + str('1') + ' ' + str(course.studentsNum)
                outputFile.write(outputRow + '\n')
            else:
                del self.data.courses[x]

    def convertToNameWithoutSpaces(self, lineCourse):
        """
        replace spaces by starts in names of course

        """
        s = lineCourse.split(' ')
        lineToWrite = '*'.join(s[:-4])
        lineToWrite += ' '+ ' '.join(s[-4:])
        return lineToWrite

    def convertName(self, name):
        """
        replace spaces by stars in names

        """
        s = name.split(' ')
        lineToWrite = '*'.join(s)
        return lineToWrite

    def writeToOutputFile(self):
        """
        create output file with school data in format defined in International Timetabling Competition 2007
        
        """
        pathOutputFile = "/home/kasia/PycharmProjects/DataParsing/OutputDataSchool/comp22.ctt"
        outputFile= open(pathOutputFile, 'w')
        outputFile.write('Name: SchoolData' + '\n')
        outputFile.write('Courses: ' + str(len(self.data.courses)) + '\n')
        outputFile.write('Rooms: ' + str(len(self.data.rooms)) + '\n')
        outputFile.write('Days: 5' + '\n')
        outputFile.write('Periods_per_day: 15' + '\n')
        outputFile.write('Curricula: ' + str(len(self.data.curricula)) + '\n')
        outputFile.write('Constraints: 0' + '\n')
        outputFile.write('\n')
        outputFile.write('COURSES:' + '\n')
        pathCoursesFile = "/home/kasia/PycharmProjects/DataParsing/OutputDataSchool/courses2.csv"
        ins = open(pathCoursesFile, "r" )
        for line in ins:
            lineToWrite = self.convertToNameWithoutSpaces(line)
            outputFile.write(lineToWrite)
        outputFile.write('\n')

        outputFile.write('ROOMS:' + '\n')
        for x in self.data.rooms:
            room = self.data.rooms[x]
            outputFile.write(self.convertName(room.id) + '\t' + str(room.capacity) + '\t' + room.type + '\n')

        outputFile.write('\n')
        outputFile.write('CURRICULA:' + '\n')
        for x in self.data.curricula:
            curricula = self.data.curricula[x]
            curricula.courseNum = len(curricula.members)
            outputString = self.convertName(curricula.id) + '  ' + str(curricula.courseNum)

            for mem in curricula.members:
                for x in self.data.courses.keys():
                    if x == mem:
                        outputString += ' '
                        outputString = outputString + self.convertName(mem)

            outputFile.write(outputString + '\n')

        outputFile.write('\n')
        outputFile.write('UNAVAILABILITY_CONSTRAINTS:' + '\n')
        outputFile.write('\n')
        outputFile.write('END.')




