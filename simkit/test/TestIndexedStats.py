from simkit.stats import IndexedSimpleStatsTally
from simkit.base import IndexedStateChangeEvent
from simkit.base import SimEntityBase
from simkit.rand import RandomVariate

source = SimEntityBase()
print(source.describe())

name = 'foo'
rv = RandomVariate.instance('Exponential', mean=2.3)

stats = IndexedSimpleStatsTally(name)
for i in range(1000):
    for j in range(4):
        event = IndexedStateChangeEvent(j, source, name, rv.generate())
        stats.state_change(event)

print(stats)
