from simkit.simkit import EventList
from simkit.rand import RandomVariate
from simkit.simutil import SimpleStateChangeDumper
from simkit.simkit import Adapter
from examples.transferline import TransferLine
from examples.transferline import JobCreator
from examples.transferline import JobCreator

job_creator = JobCreator(RandomVariate.instance('Exponential', mean=1.7))
print(job_creator.describe())

number_stations = 3
number_machines = [5, 4, 2]
service_times = [RandomVariate.instance('Gamma', alpha=3.2, beta=2.3), \
                 RandomVariate.instance('Uniform', min=4.5, max=6.7),
                 RandomVariate.instance('Exponential', mean=3.0)]
transfer_line = TransferLine(number_stations, number_machines, service_times)
print(transfer_line.describe())

adapter = Adapter('job_arrival', 'arrival')
adapter.connect(job_creator, transfer_line)

transfer_line.add_state_change_listener(SimpleStateChangeDumper())

# EventList.stopAtTime(20.0)

EventList.stop_on_event(10, 'job_complete')

EventList.verbose = True
EventList.reset()
EventList.start_simulation()