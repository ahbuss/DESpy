from simkit.simkit import EventList

EventList.verbose = True
EventList.stopAtTime(20.0)

EventList.reset()
EventList.startSimulation()

EventList.stopAtTime(10.0)
EventList.reset()
EventList.startSimulation()