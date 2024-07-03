# Tests Report

```text
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.2.2, pluggy-1.5.0
rootdir: /home/davide/workspace/cachorro
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.2.0, cov-5.0.0
collected 2 items

tests/test_decorators.py ..                                              [100%]

---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
cachorro/__init__.py         4      0   100%
cachorro/decorators.py      37      8    78%   26, 38-44, 59
cachorro/utils.py           53     35    34%   59-66, 95-111, 134-145
------------------------------------------------------
TOTAL                       94     43    54%


============================== 2 passed in 2.16s ===============================

```
