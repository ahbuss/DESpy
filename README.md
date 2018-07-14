# DESpy
__DESpy__ is an implementation in Python 3.7 of Schruben's Event Graph Methodology, loosely based on the Java Simkit package.

## Installation

* Install Python 3.7 or greater
* Install __DESpy__ module [link forthcoming]

## Running Example Scenarios
The sample components are in the ``examples`` package, with the 
sample scenarios in the ``examples.run`` package
* SimpleServer
* FiniteCapacityServer
* EntityServer
* ServerWithReneges
* TransferLine
* TwoCranesBerth
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
|Run for xxx simTime units|``EventList.stop_at_time(xxx)``|
|Run for n Foo events|``EventList.stop_on_event(n, 'Foo')``
|Prepare for running model|``EventList.reset()``|
|Run Model|``EventList.start_simulation()``|

## Running Multiple Replications

```
for replication in range(number_replications):
    EventList.reset()
    EventList.startSimulation()
    ```

* Inner vs outer stats

## Parameters vs State Variables

### Defining Events

### RandomVariate Instantiation
