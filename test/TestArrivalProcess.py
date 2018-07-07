from simkit.rand import Exponential
from examples.arrivalprocess import ArrivalProcess
from simkit.simkit import EventList
from simkit.simutil import SimpleStateChangeDumper

if __name__=="__main__":
    generator = Exponential(1.7)
    arrivalProcess = ArrivalProcess(generator)
    print(arrivalProcess)

    print(type(arrivalProcess))

    dumper = SimpleStateChangeDumper()
    arrivalProcess.addStateChangeListener(dumper)

    EventList.stopAtTime(10.0)

    EventList.verbose = True

    EventList.reset()
    EventList.startSimulation()