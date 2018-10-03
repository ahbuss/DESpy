# DESpy
**DESpy** is a Python implementation of Discrete Event Simulation 
(DES) methodology based on Schruben's Event Graphs (see [Simulation Modeling with Event Graphs](http://delivery.acm.org/10.1145/360000/358460/p957-schruben.pdf)).
It also suports the LEGO component framework (see [Building Complex Models with LEGOs](https://www.informs-sim.org/wsc02papers/094.pdf) and [Component Based Simulation Modeling with Simkit](https://www.informs-sim.org/wsc02papers/031.pdf)).


## Installation

* Python 3.7 or greater installed
* `pip install DESpy`

## Running Example Scenarios
The sample components are in the ``examples`` package, with the 
sample scenarios in the ``examples.run`` package
* SimpleServer
* FiniteCapacityServer
* EntityServer
* ServerWithReneges
* TransferLine
* Confidence Interval Example: terminating case
* Confidence Interval Example: steady-state case

## Defining an Event Graph Component
Each Event Graph component corresponds to a specific element in a DESpy model

|Event Graph|DESpy|
|-----------|-----|
|Component  |Subclass of SimEntityBase|
|Parameter  |attribute passed in to`` __init()__``|
|State variable| attribute initialized to ``nan`` or ``[]``|
|Run Event| ``reset()`` method and ``run()`` method|
|Other Events|method of same name, first letter lower-case|
|State transition|assignment to state variable followed by ``notify_state_change()``|
|Schedule event|call ``schedule(<event name>, <delay>, [<optional parameters>])``|
|Cancel event|call ``cancel(<event name>, [<optional arguments>]`` |

## Executing Model

|Action|EventList call|
|------|--------------|
|Run verbose mode|``EventList.verbose=True``|
|Run for xxx simtime units|``EventList.stop_at_time(xxx)``|
|Run for n Foo events|``EventList.stop_on_event(n, 'Foo')``
|Prepare for running model|``EventList.reset()``|
|Run Model|``EventList.start_simulation()``|

## Example: SimpleServer

The `SimpleServer` component is the most basic implementation of a multiple
server queue. Its state representation consists of integers representing the
number of customers in queue (`number_in_queue`) and the number of available
servers (`number_available_servers`). It is not a stand-alone model, but must be 
set up to "listen" to another component that periodically schedules an `Arrival` event.
The most basic such component is the `ArrivalProcess`.

```
# Instantiate ArrivalProcess component with interarrival times Exponential(1.7)
interarrival_time_generator = RandomVariate.instance('Exponential', mean=1.7)
arrival_process = ArrivalProcess(interarrival_time_generator)

# Instantiate SimpleServer component with 2 servers and service times Gamma(1.7, 1.8)
number_servers = 2;
service_time_generator = RandomVariate.instance('Gamma', alpha=1.7, beta=1.8)
simple_server = SimpleServer(number_servers, service_time_generator)

# Add the SimpleServer instance to the ArrivalProcess instance as a
# SimEventListener
arrival_process.add_sim_event_listener(simple_server)

# These statistics objects will collect the time-varying number_in_queue
# and number_available_servers of the SimpleServer instance
number_in_queue_stat = SimpleStatsTimeVarying('number_in_queue')
number_available_servers_stat = SimpleStatsTimeVarying('number_available_servers')

# Add the statistics objects as StateChangeListeners
simple_server.add_state_change_listener(number_in_queue_stat)
simple_server.add_state_change_listener(number_available_servers_stat)

# Execute the model for 100,000 time units
stopTime = 100000;
EventList.stop_at_time(stopTime)

# Initialize the EventList and put all Run events on the EventList
EventList.reset()

# Execute the simulation
EventList.start_simulation()
```

## Running Multiple Replications

The most straightforward way to estimate confidence intervals is by running
multiple independent replications. 
To run multiple replications, wrap the ``reset()`` and ``start_simulation()``
calls in a ``for`` loop. Collecting statistics, however, needs to be different
for the "inner" statistics objects and "outer" ones.
   
Statistics objects are ``StateChangeListeners`` that implement the ``stateChange()`` method
to update their counters. The two main types are "tally" and "time-varying."
They are typically used in tow different ways: "inner" and "outer." 

An **Inner** statistics object uses state trajectories from a single replication to 
produce a value - typically a mean - for that replication. Since simulation data
are tyically auto-correlated, estimates of the variance can be extremely biased.
Thus, the usual expression for a confidence interval cannot be applied.
It is important to `clear()` each inner statistics object
before each replication in order to ensure independence between replications.

An **Outer** statistics object is typically used to collect data from the inner
statistics objects. After each replication, a value from an inner statistics
object (often the mean) is passed to the outer object. 

In this manner, regardless of the value passed, the outer statistics object
can then (with sufficient quantity of replications) produce a confidence interval for the 
value in question (with all the "usual" assumptions about the central limit theorem). 

### Parameters vs State Variables

## Parameters

Parameters are variables in a component that do not change during a given replication of
the simulation. These are inputs to the simulation and, as such, must be 
passed in via the `__init()__` method. Parameters may be scalars, such as the
total number of servers, or RandomVariates which generate different values
on each call, such as the service time generator. In such cases, while the generated values may be different,
the distribution itself remains the same.

## State Variables

State variables _do_ change within a given replication of a model. The full
definition of a state variable must include its initial value, since that 
is set in the `reset()` method of each component. Only event methods are
permitted to change the value of a state variable, since events are identified with state transitions. Thus, the value of a given
state at any point in simulated time is completely determinded by its 
initial value and the subsequent state transitions.

Every state transition must be accompanied by a `notify_state_change()` call, which 
notifies StateChangeListsners that the given state has changed. This allows
components to be written to the dynamics of the model only and not be concerned with
collecting statistics, since that can be done with the appropriate statistical
objects, which are StateChanegListsners.

### Defining Events

An Event is defined in a subclass of `SimEntityBase` as simply an ordinary method. Within an event method,
there should only be (in order):

1. State transitions (followed by state change notifications)
2. Canceling events (if needed) by a call to `self.cancel()`
3. Scheduling events (if needed) by a call to `self.sechedule()`

### RandomVariate Instantiation

By convention, a `RandomVariate` class specifies its parameters as named ones in the 
constructor. 

There are several ways to instantiate a `RandomVariate`. 

* Direct instantiation, e.g. `Exponential(mean=2.3)`
* Using the `RandomVariate` factory method with keywords: `RandomVariate.instance('Exponential', mean=2.3)`
* Using the RandomVariate factory method with a dictionary (using the `params` keyword):
```
params_map={mean:2.3}
RandomVariate.instance('Exponential', params=params_map)
```

