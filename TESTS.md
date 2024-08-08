# Tests Report

```text
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0
rootdir: /home/davide/workspace/cachorro
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.2.0, cov-5.0.0, time-machine-2.14.2
collected 2 items

tests/test_decorators.py ..                                              [100%]

---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
cachorro/__init__.py         4      0   100%
cachorro/decorators.py      86     43    50%   28, 40-46, 61, 87-89, 109-118, 130-134, 154-155, 187, 206-232, 244-251, 280-281
cachorro/utils.py           53     35    34%   59-66, 95-111, 134-145
------------------------------------------------------
TOTAL                      143     78    45%


============================== 2 passed in 2.13s ===============================

```
