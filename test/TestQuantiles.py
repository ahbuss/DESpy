from simkit.quantiles import normal
from simkit.quantiles import student_t

p = 0.0
# print('Normal quantiles:')
# while p < 1.0:
#     print('{p:,.3f}\t{q:,.8f}'.format(p=p, q=NormalQuantile.quantile(p)))
#     p += 0.005
# print(NormalQuantile.quantile(-.2))
# print(NormalQuantile.quantile(1.1))
print('StudentT quantiles:')

p = 0.005
p = 1-p
print('p={p:.3f}'.format(p=p))
for df in range(100):
    print(str(df) + '\t' + str(student_t(p, df)))
