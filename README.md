# Chat50 Server

![Python application](https://github.com/michaelpaul/chat50-server/workflows/Python%20application/badge.svg)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/michaelpaul/chat50-server)

A Python chat server using Flask and Socket.IO.

Checkout the frontend at: https://github.com/michaelpaul/chat50-ui

## Local Development

Run the commands from `.gitpod.yml` to setup the environment and then run:

- `docker-compose up` - Start backing services
- `heroku local` - Start the app


## Test

- `pip install '.[test]'`
- `pytest`

Run with coverage report::

- `coverage run -m pytest`
- `coverage report`
- `coverage html` - open htmlcov/index.html in a browser
