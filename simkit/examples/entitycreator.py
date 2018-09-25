from simkit.base import SimEntityBase
from simkit.base import Entity
from simkit.base import Priority

class EntityCreator(SimEntityBase):

    def __init__(self, generator):
        SimEntityBase.__init__(self)
        self.generator = generator

    def run(self):
        self.schedule('generate', self.generator.generate())

    def generate(self):
        self.schedule('generate', self.generator.generate())
        self.schedule('arrival', 0.0, Entity())

    def doArrival(self, entity):
        pass
