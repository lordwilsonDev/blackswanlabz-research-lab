# Q2B-MBEDDR-002 Verifier Adapter Contract v0.1

The independently executable verifier expects the learner artifact to expose a
narrow adapter interface.

## Required functions

`create_controller()` returns a controller object exposing:

- `add_state(name, initial=False)`
- `add_transition(source, event, destination, guard=None)`
- `quantity(value, unit)`
- `compare(left, right)`
- `set_environment(**values)`
- `dispatch(event)`
- `current_state`
- `verify_reachability()`
- `verify_guards(probes)`

Quantity objects expose:

- `dimension`
- `to_si()`

The verifier is bounded and does not claim formal proof.

The adapter is a verification interface, not a learner hint about the hidden
implementation. The task's required behavior remains the semantic target.
