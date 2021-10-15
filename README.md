# Continuous Performance Testing

This is an example of performance testing that can be run in a UI mode or in a CLI mode.

## UI Mode

This can be started with `make run-locust`  It will start the test server and the performance
test in "UI" mode that allows the user to try it out at http://localhost:8089


## CLI/Test Mode

This mode is such that a performance test can be run with assertions to verify:
- calls per second are at a minimum threshold
- errors are at a minimum threshold
- p50 and p95 latency are at or below a certain threshold.

This can be run with the command `make test-locust`