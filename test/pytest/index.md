# pytest

## how to get list of failure at the end of test?

* use `pytest_sessionfinish` and `pytest_runtest_logreport`
```python
#conftest.py

def pytest_runtest_logreport(report):
  '''收集错误信息'''
  if report.when == 'call' and report.failed:
    error_reports.append(report)

def pytest_sessionfinish(session, exitstatus):
  '''错误信息报警'''
  if not hasattr(session.config, 'workeroutput'):
    db = pymysql.connect('localhost', 'root', '', 'engine_monitor')
    with db.cursor() as cursor:
        cursor.executemany('insert into mo_error (module, nodeid, error_message, url, time) values (%s, %s, %s, %s, %s)', values)
    db.commit()
    db.close()
```

## how to distinguish master/worker process in pytest_session_finish?
if `session.config` has attr `workeroutput`, then it's worker 

## 如何减少重复的参数
```python
import pytest


@pytest.mark.parametrize('common_arg1', [0, 1])
@pytest.mark.parametrize('common_arg2', [2, 3])
class TestParametrized:

    @pytest.mark.parametrize('a', [0, 1])
    def test_1(self, common_arg1, common_arg2, a):
        pass

    @pytest.mark.parametrize('b', [0, 1])
    def test_2(self, common_arg1, common_arg2, b):
        pass

    @pytest.mark.parametrize('x', [0, 1])
    def test_100(self, common_arg1, common_arg2, x):
        pass
```

https://stackoverflow.com/questions/51739589/pytest-how-to-share-parametrized-arguments-across-multiple-test-functions