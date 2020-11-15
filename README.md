# AutoFAQ widget/API tests

# Widget tests:
pytest.exe .\tests\test_widget.py -vv

# API tests:
pytest.exe --token=USER_TOKEN .\tests\test_api.py -vv

# Additional:
Widget tests are looking for executable of webdriver in the root project directory by default.

Your user token is provided via --token=USER_TOKEN option