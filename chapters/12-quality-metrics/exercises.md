# Chapter 12 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks
you to reason; a **[calculation]** tag marks exercises that require working the
numbers. At least five exercises require calculation — show your
work, including formulas and intermediate values, not just a final number.

Two datasets recur (the same ones used in the chapter). **Dataset A** is a univariate
series of customer-found defects for eleven releases; **Dataset B** pairs module size
with defects.

- **Dataset A** (sorted): $2,\ 4,\ 5,\ 5,\ 7,\ 8,\ 9,\ 10,\ 12,\ 14,\ 23$
- **Dataset B:** $x$ (KLOC) $= 2, 4, 6, 8, 10$; $y$ (defects) $= 5, 9, 10, 13, 18$

## Concepts

1. **[warm‑up]** In your own words, distinguish an *entity*, an *attribute*, and a
   *metric*. Give two different metrics for the same attribute of a source file, and say
   why one might be more *valid* than the other.
2. **[warm‑up]** Classify each of the following by scale of measurement (nominal,
   ordinal, interval, or ratio) and name one statistic that is *legal* and one that is
   *illegal* for it: (a) defect severity S1–S4, (b) defect count per release, (c) the
   calendar date a bug was filed, (d) the module a bug lives in.
3. **[warm‑up]** State the difference between a *bar chart* and a *histogram*. Give one
   dataset that belongs on each, and explain why swapping them would mislead.
4. **[warm‑up]** Write the GQM for this goal: "reduce the time new engineers take to make
   their first safe production change." Supply at least one *question* and two *metrics*,
   and name a *counter-metric* that would catch someone gaming one of them.

## Analysis

5. **[analysis]** A manager proposes paying testers a bonus per bug they file. Using
   Goodhart's Law and the idea of a counter-metric, predict two specific ways this will
   distort behavior, and propose a metric pair that resists the distortion.
6. **[analysis]** Two releases each report exactly 30 customer-found defects. Release P
   runs on 5,000 installs; release Q runs on 500,000 installs. Explain, with a normalized
   figure for each, why raw CFD count makes them look equal when their quality is very
   different. State which release is cleaner and by how much.
7. **[analysis]** The chapter says severity is *ordinal* and should not be averaged. A
   colleague insists "average severity 2.7" is fine because the labels map to numbers
   1–4. Rebut this in two or three sentences, and propose what to report instead.
8. **[analysis]** Explain the difference between DRE improving because your *product* got
   better and the customer quality metric $Q_{\text{cust}}$ falling because *usage*
   dropped. Which metric is confounded by usage and which is not? Why does Northwind track
   both (§12.5)?
9. **[analysis]** You compute a 95% confidence interval $(5.07, 12.93)$ for a release's
   mean CFD count. A teammate says "so there's a 95% chance the true mean is between 5.07
   and 12.93." Explain precisely why this interpretation is wrong and give the correct
   one.

## Calculation

10. **[analysis][calculation]** *(Defect-removal efficiency.)* During development, reviews
    and testing remove 465 defects. In the first six months of production, customers
    report 35 more. (a) Compute DRE. (b) The team's goal is 95% DRE; how many *fewer*
    escaped defects (holding $D_{\text{before}}$ fixed) would they have needed to hit it?
    (c) Explain why DRE for this release is still "provisional" at six months.
11. **[analysis][calculation]** *(Quartiles and boxplot.)* For **Dataset A**, compute the
    five-number summary (min, Q1, median, Q3, max), the IQR, and the upper and lower
    outlier fences. Identify any outliers, state where each whisker ends, and say whether
    the distribution is left- or right-skewed and how you can tell from the summary.
12. **[analysis][calculation]** *(Variance and standard deviation.)* For **Dataset A**,
    compute the mean, the sample variance $s^2$, and the sample standard deviation $s$,
    showing the deviation table. Then recompute the variance *dividing by $n$ instead of
    $n-1$*. Explain which is appropriate if the eleven values are (a) a sample from an
    ongoing process, versus (b) the entire population of releases ever shipped.
13. **[analysis][calculation]** *(z-interval.)* You measure $n = 64$ builds and get a
    sample mean duration of $\bar{x} = 8.0$ minutes. From long history the population
    standard deviation is known to be $\sigma = 2.4$ minutes. Construct the 95% z-interval
    for the true mean build time (use $z^\* = 1.96$). Then state what would happen to the
    interval's width if you quadrupled the sample size to 256, and by what factor.
14. **[analysis][calculation]** *(t-interval.)* A different eight-release sample of CFD
    counts has $\bar{x} = 11$ and $s = 4.0$. Using $t^\*_{7} = 2.365$ for 95% confidence,
    construct the t-interval for the mean. Then explain in one sentence why you used a
    t-value larger than 1.96 rather than the normal critical value.
15. **[analysis][calculation]** *(OLS regression.)* For **Dataset B**, fit the
    least-squares line $\hat{y} = b_0 + b_1 x$. Show $\bar{x}$, $\bar{y}$, $S_{xy}$,
    $S_{xx}$, then $b_1$ and $b_0$. Compute the residual for the $x = 4$ point, the SSE,
    and $R^2$. Interpret the slope in plain words, and explain why predicting $y$ at
    $x = 40$ from this fit would be unwise.
