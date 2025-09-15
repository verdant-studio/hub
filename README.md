# Hub

Aggregate, monitor, and act on data from all your WordPress sites in one place.

<img width="1008" alt="screenshot" src="https://github.com/user-attachments/assets/71246156-830c-4056-832e-e1869a17f7a9" />

## About

Hub lets you monitor your WordPress websites and their status from one place.

This project is designed to be used alongside the [Relay](https://wordpress.org/plugins/relay/) WordPress plugin.

## Features

- Fetch and show:
  - Health rating
  - WordPress version
  - Updates available
  - Directory sizes
  - Multisite and subsite
- Sorting
- Searching (search includes subsites)
- Add maintainers
- Add comments

## Getting started

### Option 1. Docker

```sh
# run docker compose
docker compose up --build

# stop containers
docker compose down

# optional: stop and remove everything including volumes
docker compose down --volumes --remove-orphans
```

### Option 2. Manual

#### Server

```sh
# copy the .env.example to .env
cp .env.example .env

# create virtual environment
cd server && python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install api dependencies
pip install -r requirements.txt

# start uvicorn
uvicorn main:app --port=2000 --reload
```

The API docs are available at [http://127.0.0.1:2000/docs](http://127.0.0.1:8000/docs).

#### Client

```sh
# install dependencies
cd client && npm i

# other commands
npm run format
npm run dev
```

## Documentation

View the [documentation](https://docs.verdant.studio/hub/) for more information.
