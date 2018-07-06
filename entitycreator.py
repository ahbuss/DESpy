from simkit import SimEntityBase
from simkit import Entity

class EntityCreator(SimEntityBase):

    def __init__(self, generator):
        SimEntityBase.__init__(self)
        self.generator = generator

    def doRun(self):
        self.waitDelay('Generate', self.generator.generate())

    def doGenerate(self):
        self.waitDelay('Generate', self.generator.generate())
        self.waitDelay('Arrival', 0.0, Entity())

    def doArrival(self, entity):
        pass
