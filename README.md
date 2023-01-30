# TEAM International
Python dev test by Juan Argaez, 01/25/2023

### Requirements

1. A `DataCapture` class can `add` numbers in the range between 0-999.
1. When invoking `build_stats`, an object is returned supporting `greater`, `less` and `between` methods to query stats.

### Design

#### Functional Core

Following a functional approach and the clean/onion architecture, there is a core module with business domain types and
operations as functions. This has advantage of having succinct code, easy to understand, test and maintain. Also
inherits the principle of making illegal states unrepresentable. For instance, at this core there is no code path to
build stats when numbers are not captured yet.

Having the core composed of pure functions and immutable data, gives confidence that state won't be corrupted by illegal
states bugs. Also, `Result` container is used to represent success or failure of an operation, so caller decides how to
handle non success cases.

With above benefits, technical debt is reduced.

#### Object-Oriented API

Since two objects are required to interface with capturing numbers and querying stats, there is a module to expose this
functionality interoperable with the functional core and exposed as objects for OOP.

* `DataCapture` class has `add` and `build_stats` methods.
* `DataCaptureStats` is returned by `build_stats` and has the required methods to query stats.

### Algorithms complexity

As requested, computing stats is done in O(N) time complexity traversing once the captured numbers. Then stats querying
is supported in O(1). Space complexity is O(N) as stats are stored for each captured number.

### Testing

Quality is assured by Property Based Testing. The key advantage is that correctness is proved by logic properties with
random generated data in each run.

Unit testing was integrated with random generated data also to test expected errors are raised.

### Dependencies

* Python 3.11.1
* Packages in requirements.txt

### REPL

Load `ooapi/data_capture.py` in an interactive Python session and execute for testing:

```python
capture = DataCapture()
capture.add(3)
capture.add(9)
capture.add(3)
capture.add(4)
capture.add(6)

stats = capture.build_stats()
stats.less(4) # should return 2 (only two values 3, 3 are less than 4)
stats.between(3, 6) # should return 4 (3, 3, 4 and 6 are between 3 and 6)
stats.greater(4) # should return 2 (6 and 9 are the only two values greater than 4)
```
