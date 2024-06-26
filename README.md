# Cachorro

Cachorro is a simple Python library mainly used to cache the returns of some functions.

![Test Coverage](https://img.shields.io/badge/Tests-PASSED-brightgreen?style=plastic&labelColor=blue)
![Version](https://img.shields.io/badge/Version-0.0.1-blue?style=plastic)
![MIT License](https://img.shields.io/badge/License-MIT-blue?style=plastic)

## Installation

```bash
pip install cachorro
```

## Usage

```python
from cachorro import cacheme
from time import sleep

@cacheme
def test_func(arr):
    print("going to sleep")
    sleep(5)
    print("awaken")
    return [x * 2 for x in arr]

result_1 = test_func(self.initial_vector) # the firs time around it executes the function
result_2 = test_func(self.initial_vector) # the second time around it returns the cached results
```

## Tests

For the latest report on tests coverage, see the [TESTS.md](TESTS.md).

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

Released under MIT License.

Please read [LICENSE](LICENSE) for details about cachorro's license.
