from simkit.stats import SimpleStatsTally
from math import nan

sst = SimpleStatsTally("test");
sst.new_observation(nan)

print(sst)

for x in range(1,11):
    sst.new_observation(x)
    sst.new_observation(nan)

print(sst)