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
|Run for xxx simtime units|``EventList.stop_at_time(xxx)``|
|Run for n Foo events|``EventList.stop_on_event(n, 'Foo')``
|Prepare for running model|``EventList.reset()``|
|Run Model|``EventList.start_simulation()``|

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

### Defining Events

### RandomVariate Instantiation
