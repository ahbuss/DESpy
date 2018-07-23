from simkit.simkit import EventList

EventList.verbose = True
EventList.stop_at_time(20.0)

EventList.reset()
EventList.start_simulation()

EventList.stop_at_time(10.0)
EventList.reset()
EventList.start_simulation()