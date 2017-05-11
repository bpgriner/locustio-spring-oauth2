# Locust.io & Spring OAuth2
- This is an example Locust.io load testing application demonstrating how to interact with a Spring OAuth2 REST API.
- This is only a reference implementation and will need to be modified to work with your web application.

# Tech
- Locust.io → http://locust.io
- Spring OAuth2 → https://spring.io/guides/tutorials/spring-boot-oauth2
- Python → https://www.python.org
- Pip → bundled with Python 2.7+
- Virtualenv → https://virtualenv.pypa.io

# Run
Must Have Python installed (version 2.7+)

1.  `$ pip install virtualenv`  (this installs virtualenv globally)
2.  change to directory where `locust-test.py` lives
3.  `$ virtualenv venv` (creates a virtualenv folder labeled `venv`)
4.  `$ source venv/bin/activate` (activate virtual environment)
5.  `$ pip install -r requirements.txt` (this installs all dependencies into `venv` only)
6.  `$ locust -f locust-test.py` (start locust w/ python test file)
7.  open a browser and goto `http://localhost:8089`

To close locust: `Ctrl+c` via command line

To escape from the virtual environment: `$ deactivate`
