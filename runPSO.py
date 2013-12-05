import time
import sys

from cats.pso.timetable import TimetableFactory
from cats.utils.data import Data
from cats.readers.competitionReader import CompetitionReader
from cats.pso.particle import Particle
from cats.pso.pso import PSO

fileName = sys.argv[1]
timeLimit = float(sys.argv[2])
endTime = time.time() + timeLimit

c = CompetitionReader()
data = c.read(fileName)

pso = PSO(data, endTime)
best = pso.run()

print best.penalty


