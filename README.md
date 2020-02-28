# SatSolver

The code uploaded is for a modified version of the WALKSAT algorithm. After a failed run for maxit assignments, the number of variables to be flipped at each iteration is incremented by 1, upto a maximum. The set S of variables that are present in the clauses that are FALSE is found. Following this, we randomly select v variables from the set S, and flip their values with probability p. (If set S contains less than v variables, then we flip all the variables in S with probability p.) Otherwise, with probability (1 − p) we flip v variables such that the number of FALSE clauses are minimized.

We run this algorithm for a sufficient number of runs on randomly 3 generated SAT instances, to obtain a performance graph.
