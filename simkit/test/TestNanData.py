from simkit.stats import SimpleStatsTally
from math import nan

simple_stats_tally = SimpleStatsTally()
simple_stats_tally.new_observation(nan)
simple_stats_tally.new_observation(1)
simple_stats_tally.new_observation(2)
print(simple_stats_tally)
