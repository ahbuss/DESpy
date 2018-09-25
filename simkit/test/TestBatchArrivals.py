from simkit.rand import RandomVariate
from simkit.base import EventList
from simkit.base import Adapter
from simkit.simutil import SimpleStateChangeDumper
from simkit.examples.arrivalprocess import BatchArrivalProcess
from simkit.examples.simpleserver import SimpleServer

interarrival_time_generator = RandomVariate.instance('Exponential', mean=2.5)
batch_generator = RandomVariate.instance('Discrete', values=[1, 2, 3, 4, 5], \
                                         frequencies=[20, 30, 40, 50, 60])
batch_arrival_process = BatchArrivalProcess(interarrival_time_generator, batch_generator)
print(batch_arrival_process.describe())

number_servers = 1
service_time_generator = RandomVariate.instance('Gamma', alpha=1.2, beta = 2.3)
simple_server = SimpleServer(number_servers, service_time_generator)
print(simple_server.describe())

adapter = Adapter('arrival1', 'arrival')
adapter.connect(batch_arrival_process, simple_server)

batch_arrival_process.add_state_change_listener(SimpleStateChangeDumper())
simple_server.add_state_change_listener(SimpleStateChangeDumper())

stopTime = 20.0

EventList.verbose = True
EventList.stop_at_time(stopTime)
EventList.stop_on_event(10, 'arrival')

EventList.reset()
EventList.start_simulation()