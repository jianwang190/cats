from cats.readers.competitionReader import CompetitionDictReader
from cats.utils.timetable import TimeTable, TimeTableFactory
from cats.adaptiveTabuSearch.heuristics import initialSolution

def main():
    c = CompetitionDictReader()
    data = c.readInstance(1)
    t = TimeTableFactory.getTimeTable(data)


    initialSolution(t, data)


if __name__=="__main__":
    main()