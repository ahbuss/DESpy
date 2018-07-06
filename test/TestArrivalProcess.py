from rand import Exponential
from arrivalprocess import ArrivalProcess
from simkit import EventList
from simutil import SimpleStateChangeDumper

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