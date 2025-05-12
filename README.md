# Hub

> Aggregate, monitor, and act on data from all your WordPress sites in one place.

## About

Hub lets you monitor your WordPress websites and their status from one place.

This project is designed to be used alongside the [Relay](https://wordpress.org/plugins/relay/) WordPress plugin.

## Features

- List websites and display their health rating, available updates, WordPress version and subsite information
- Add maintainers

## Getting started

### Server

```sh
# create virtual environment
cd server && python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install api dependencies
pip install -r requirements.txt

# start uvicorn
uvicorn main:app --reload
```

The API docs are available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Client

```sh
# install dependencies
cd client && npm i

# other commands
npm run format
npm run dev
```

## Documentation

View the [documentation](https://docs.verdant.studio/hub/) for more information.