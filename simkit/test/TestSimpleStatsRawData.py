from simkit.stats import SimpleStatsTallyRawData
from simkit.stats import SimpleStatsTally

sstrd = SimpleStatsTallyRawData()
sst = SimpleStatsTally()
for x in range(1,11):
    sstrd.new_observation(x)
    sst.new_observation(x)
print(sstrd.raw_data)
print (sst)