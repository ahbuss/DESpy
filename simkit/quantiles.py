from math import pi
from math import sqrt
from math import fabs
from math import inf
from math import log
from math import tan
from math import pow
from math import exp
from math import nan

# Rather than have a dependence on bigger packages, for simple computations of confidence intervals and
# hypothesis tests for means, the Normal and Student T quantiles only are implemented here.
# For more extensive statistical actions use an appropriate package (like scipy) or connect to R
from unicodedata import name

A0 = 2.50662823884
A1 = -18.61500062529
A2 = 41.39119773534
A3 = -25.44106049637
B1 = -8.47351093090
B2 = 23.08336743743
B3 = -21.06224101826
B4 = 3.13082909833
C0 = -2.78718931138
C1 = -2.29796479134
C2 = 4.85014127135
C3 = 2.32121276858
D1 = 3.54388924762
D2 = 1.63706781897
SPLIT = 0.42

    # Based on Beasley & Springer, "Algorithm AS 111: The Percentage Points of the Normal Distribution",
    # Journal of the Royal Statistical Society. Series  C(Applied Statistics) Vol. 26, No 1.
def normal(p):
    if p < 0.0 or p > 1.0:
        raise ValueError('p must be in [0.0, 1.0]: ' + str(p))
    if p == 0.0:
        quantile = -inf
    elif p == 1.0:
        quantile = inf
    elif p == 0.5:
        quantile = 0.0
    else:
        q = p - 0.5
        if (fabs(q) < SPLIT):
            r = q * q
            quantile = q * (((A3 * r + A2) * r + A1) * r + A0) \
                        / ((((B4 * r + B3) * r + B2) * r + B1) * r + 1.0)
        else:
            if q <= 0.0:
                r = p
            else:
                r = 1.0 - p
            r = sqrt(-log(r))
            quantile = (((C3 * r + C2) * r + C1) * r + C0) \
                    / ((D2 * r + D1) * r + 1.0);
            if q < 0.0:
                quantile = -quantile
    return quantile


    # Based on Hill, G.W., "Algorithm 396 Student T Quantiles," Communications of the ACM,
    # Vol 13, No. 10, October 1970.
    # Returns nan if df = 0
def student_t(p, df):
    if df < 0:
        raise ValueError('df must be > 0: ' + str(df))
    if p < 0.0 or p > 1.0:
        raise ValueError('p must be >= 0: ' + str(p))
    if df == 0:
        return nan
    p = 2.0 * p
    if p == 0.0:
        quantile = -inf
    elif p == 2.0:
        quantile = inf
    elif p == 1.0:
        quantile = 0.5
    elif df == 1:
        quantile = -1.0 / tan(p * 0.5 * pi)
    elif df == 2:
        quantile = sqrt(2.0 / (p * (2.0 - p)) - 2.0)
    else:
        a = 1.0 / (df - 0.5)
        b = 48.0 / (a * a)
        c = ((20700.0 * a / b - 98.0) * a - 16.0) * a + 96.3
        d = ((94.5 / (b + c) - 3.0) / b + 1.0) * sqrt(a * 0.5 * pi) * df
        x = d * p
        y = pow(x, 2.0 / df)

        if y > 0.05 + a:
            x = normal(0.5 * p)
            y = x * x
            if df < 5:
                c = c + 0.3 * (df - 4.5) * (x + 0.6)
            c = (((0.05 * d * x - 5.0) * x - 7.0) * x - 2.0) * x + b + c
            y = (((((0.4 * y + 6.3) * y + 36.0) * y + 94.5) / c - y - 3.0) / b + 1.0) * x
            y = a * y * y
            #         This is the update from Hill, 1981
            if (y > 0.1):
                y = exp(y) - 1.0
            else:
                y = ((y + 4.0) * y + 112.0) * y * y / 24.0 + y
        else:
            y = ((1.0 / (((df + 6.0) / (df * y) - 0.089 * d - 8.222) * (df + 2.0) * 3.0) + 0.5 / \
                  (df + 4.0)) * y - 1.0) * (df + 1.0) / (df + 2.0) + 1.0 / y;
        quantile = sqrt(df * y)
    if (p < 0.5 and df != 1):
        quantile = -quantile
    return quantile