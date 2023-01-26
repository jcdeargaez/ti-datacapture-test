# TEAM International
Python dev test by Juan Argaez, 01/25/2023

### Requirements

1. A `DataCapture` class can `add` numbers in the range between 0-999.
1. When invoking `build_stats`, an object is returned supporting `greater`, `less` and `between` methods to query stats.

### Design

* `DataCapture` class has `add` and `build_stats` methods.
* `DataCaptureStats` is returned by `build_stats` and has the required methods to query stats.
* Domain types hold captured numbers, frequencies, stats and error events such as an invalid number, an attempt to build
stats for empty data, an attempt to query a non captured number, and so on.
* Although two classes at least were requested, a functional programming paradigm was used following Railway Oriented 
Programming. This approach makes the code concise, easier to understand and maintain. For this reason `Result` container
is used to indicate success or error of operations, then `map`ing and `bind`ing continuation logic based on the actual 
data it holds.

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
