# Hub

Aggregate, monitor, and act on data from all your WordPress sites in one place.

> [!IMPORTANT]  
> This plugin is not yet ready for production.

## About

Hub lets you monitor your WordPress websites and their status from one place.

This project is designed to be used alongside the [Relay](https://wordpress.org/plugins/relay/) WordPress plugin.

## Features

- Fetch and show:
  - Health rating,
  - WordPress version
  - Updates available
  - Multisite and subsite
- Add maintainers
- Add comments

## Getting started

### Server

```sh
# create virtual environment
cd server && python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install api dependencies
pip install -r requirements.txt

# create and set encryption key in .env
python scripts/setup_env.py

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