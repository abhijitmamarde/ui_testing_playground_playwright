# playwright_github

### Commands

```commandline
pytest -v --numprocesses auto test_ui_automation_playground.py
pytest --numprocesses 2 test_ui_automation_playground.py --headed -m onlyheaded

# repeat test executions 10 times: add param -> --count=10
pytest --numprocesses 2 test_ui_automation_playground.py --headed -m onlyheaded --count=10

# generate report, add: 
# --html=report.html --self-contained-html
pytest -v --numprocesses auto test_ui_automation_playground.py --count=10 --html=report.html --self-contained-html
```
