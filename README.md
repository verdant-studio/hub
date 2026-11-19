# Hub

Aggregate, monitor, and act on data from all your WordPress sites in one place.

<img width="1263" height="335" alt="hub-preview" src="https://github.com/user-attachments/assets/d90a8a34-34cd-49d2-ac5c-f4e000c26962" />

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
# copy the .env.example to .env
cp .env.example .env

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

# install api dependencies (requires uv: https://docs.astral.sh/uv/)
cd server && uv sync

# start uvicorn
uv run uvicorn main:app --port=2000 --reload
```

The API docs are available at [http://127.0.0.1:2000/docs](http://127.0.0.1:2000/docs).

#### Client

```sh
# install dependencies
cd client && npm i

# other commands
npm run format
npm run dev
```

The client will be available at [http://127.0.0.1:5173](http://127.0.0.1:5173).


## Documentation

View the [documentation](https://docs.verdant.studio/hub/) for more information.
