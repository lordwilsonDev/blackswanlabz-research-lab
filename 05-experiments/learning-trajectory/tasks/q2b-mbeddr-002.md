# Q2B-MBEDDR-002 — Unit-Safe Reactive Controller

## Task class

Combined capability task: physical-unit semantics + event/guard state-machine semantics.

## Participant prompt

Build a small domain-specific controller language and execution engine with the following behavior.

### Quantities

A quantity consists of a numeric magnitude and a physical unit.

Support:
- metres (m)
- kilometres (km)
- seconds (s)
- minutes (min)
- hours (h)
- compound speed units such as m/s and km/h

Quantities of compatible dimensions must be comparable after scale normalization.

Quantities with incompatible dimensions must be rejected.

### Controller

Support:
- named states,
- one initial state,
- events,
- optional guards,
- transitions,
- runtime current state.

A transition has the form:

on EVENT -> DESTINATION

or:

on EVENT if VALUE OP QUANTITY -> DESTINATION

When multiple transitions from the same state respond to the same event, preserve declaration order.

### Required capability

Create an executable controller that can represent and run:

initial Idle
state Idle:
  on START -> Moving
state Moving:
  on TICK if speed >= 10 m/s -> Fast
  on STOP -> Idle
state Fast:
  on STOP -> Idle

The engine must correctly treat 36 km/h as equal to 10 m/s, 35 km/h as below 10 m/s, and m/s versus m as dimensionally incompatible.

### Static verification

The engine must report:
- unreachable states,
- never-enabled guarded transitions for the supplied probe domain,
- guarded transitions shadowed by an earlier transition when every tested value satisfying the later guard also satisfies the earlier guard.

The verification is explicitly bounded by the supplied probe domain.

### Extension requirement

After implementing the base controller, add a new controller capability not given in the examples. The extension must preserve all previous behavior and pass fresh tests.

The implementation should be independently executable. Do not use the source repository implementation as a code template.

## Success criteria

- base behavior correct,
- dimensional comparisons correct,
- invalid dimensions rejected,
- reachability check correct,
- bounded guard verifier correct,
- structural transfer correct under different units and states,
- extension passes fresh hidden tests.

This task is designed to test composition and structural transfer, not memorization of a feature list.
