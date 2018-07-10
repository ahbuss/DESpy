from simkit.simkit import SimEntityBase
from simkit.simkit import Entity
from simkit.simkit import Priority

class EntityCreator(SimEntityBase):

    def __init__(self, generator):
        SimEntityBase.__init__(self)
        self.generator = generator

    def run(self):
        self.waitDelay('generate', self.generator.generate())

    def generate(self):
        self.waitDelay('generate', self.generator.generate())
        self.waitDelay('arrival', 0.0, Priority.DEFAULT, Entity())

    def doArrival(self, entity):
        pass
