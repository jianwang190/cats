from cats.pso.timetable import TimetableFactory
from cats.utils.data import Data
from cats.readers.competitionReader import CompetitionReader
from cats.pso.particle import Particle
from cats.pso.pso import PSO


c = CompetitionReader()
data = c.readInstance(1)
print data.curricula[1].members

pso = PSO(data)
best = pso.run()

print best.penalty


