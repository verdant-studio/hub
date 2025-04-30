# Hub

> Aggregate, monitor, and act on data from all your WordPress sites in one place.

## About

Hub lets you monitor your WordPress websites and their status from one place.

This project is designed to be used alongside the [Relay](https://github.com/verdant-studio/relay) WordPress plugin.

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

# install client dependencies
cd ../client && npm i
```

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