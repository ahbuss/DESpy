from simkit.rand import Exponential
from simkit.examples.arrivalprocess import ArrivalProcess
from simkit.examples.arrivalprocess import EntityCreator
from simkit.base import EventList
from simkit.simutil import SimpleStateChangeDumper

if __name__=="__main__":
    generator = Exponential(1.7)
    arrival_process = ArrivalProcess(generator)
    print(arrival_process)

    print(type(arrival_process))

    dumper = SimpleStateChangeDumper()
    arrival_process.add_state_change_listener(dumper)

    EventList.stop_at_time(100.0)

    EventList.verbose = True

    EventList.reset()
    EventList.start_simulation()

    EventList.cold_reset()
    EventList.stop_on_event(10, 'entity_arrival')

    entityCreator = EntityCreator(generator)

    print("With EntityCreator")
    EventList.reset()
    EventList.start_simulation()

    # This should throw a ValueError
    # arrival_process.waitDelay('Foo', -.001)