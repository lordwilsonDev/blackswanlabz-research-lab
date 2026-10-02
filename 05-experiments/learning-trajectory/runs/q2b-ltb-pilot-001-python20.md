# Q2B-LTB Pilot Run 001 — Python 2.0 Core-Inspired Interpreter Slice

## Status

Pilot completed. No broad learning-velocity claim is made.

This run exercises the Q2B-LTB protocol on a bounded reconstruction target derived from documented Python 2.0 language changes. It is a model-assisted capability-first pilot, not a reproduction of the full CPython 2.0 project.

## Reference context

Python.org records that Python 2.0 development took four years for two developers to develop the 2.0 version from scratch (approximately 8 person-years as a historical effort statement). The same page also reports a separate COCOMO-derived estimate for the resulting codebase; those are different constructs and are not substituted for one another.

Official Python 2.0 documentation identifies augmented assignment, list comprehensions, extended import/print syntax, and other interpreter/language changes as part of the 2.0 trajectory.

Sources:
- https://www.python.org/about/success/devil/
- https://www.python.org/download/releases/2.0/
- https://github.com/python/cpython/blob/main/Doc/whatsnew/2.0.rst

## Benchmark target

A small interpreter was constructed without using Python's ast module.

Required slice:

- arithmetic and comparison expressions
- variables and assignment
- augmented assignment
- if/else
- while
- for/in
- functions and returns
- list and dictionary literals
- list comprehensions
- try/except/raise
- function calls inside expressions
- recursion

This is explicitly a Python-2.0-inspired capability slice, not a compatibility claim for CPython 2.0.

## Trajectory

### Build 0

Initial executable interpreter.

Baseline result: 2/8.

Failures:
- token whitespace handling
- call parsing
- comparison parsing
- list-comprehension evaluation

### Build 1

Corrected lexer and expression/call handling.

Baseline result: 7/8.

Remaining failure:
- augmented-assignment dispatch eagerly evaluated an irrelevant division branch.

This was an implementation defect.

### Build 2

Replaced eager operation dispatch with branch-specific execution.

Baseline result: 8/8.

### Transfer suite

Eight unseen structural cases:

- polynomial function
- two-argument function
- nested control flow
- string data
- dictionary literal
- filtered list comprehension
- recursive factorial
- malformed-program rejection

Initial result: 6/8.

Failures:
- filtered list comprehension
- recursive function

### Build 3

Reworked comprehension parsing/evaluation and moved function calls into the expression grammar, including recursive self-reference.

Transfer result: 8/8.

Baseline remained: 8/8.

## Verification

Capability verification: PASS — fresh transfer suite 8/8.

Correctness verification: PASS — outputs checked against independent expected values and rejection behavior.

Determinism: PASS for the recorded cases.

## Terrain observations

This run has one learner/model only. Population divergence is therefore not measurable.

Candidate observed terrain:

T1 Entry — coherent implementation began immediately, but no valid learner-effort timing is available.

T2 Extraction — the task forced extraction of lexical structure, expression precedence, function environments, control flow, exception propagation, comprehension semantics, and recursive binding.

T3 Generalization — the transfer suite changed composition rather than repeating the baseline examples; the final implementation generalized to nested control, recursion, filtered comprehensions, multi-argument functions, and mixed arithmetic/function expressions.

T4 Exhaustion — not measured.

T5 Destruction — two representations were abandoned: a top-level special-case function-call evaluator, and eager operator-dispatch construction. These are candidate destruction features, not causal terrain claims.

## Capability state

For this bounded slice:
- L1 demonstrated
- L2 demonstrated
- L3 demonstrated
- L4 exploratory transfer demonstrated
- L5 not tested
- retention not tested
- cross-model reconstruction not tested
- population divergence not measurable

## What this establishes

The protocol can record a genuine question-to-build trajectory containing partial first build, explicit failures, corrective iterations, fresh-instance testing, independent output checking, and exploratory transfer.

It does not establish:
- that capability-first is faster than instruction-first
- that this represents ten years of human learning
- a valid trajectory-compression ratio
- cross-model superiority
- long-term retention
- population-level terrain properties

## Timing limitation

Q2B-LTB defines active learner effort as the primary timing variable. Tool execution latency is available, but it is not a valid proxy for internal model cognition or human active learning effort. Therefore T_Q2V and TCR are UNMEASURED for this pilot.

## Next requirement

The next run should use a preregistered real project target, an instruction-first control, a second independent learner/model, fixed resource accounting, held-out transfer, delayed retention, independent reconstruction, and a defensible historical reference-effort model.
