# Prompt Collection Bot

## App

The application that was used to collec the data.

### Development Setup

- run docker-compose dev setup, note that database will be rebuild for every restart

```bash
docker-compose -f docker-compose-dev.yaml up
```

### Deployment Setup

- run docker-compose with rebuilding images, currently this deletes all tables and fills them with dev data, database itself will be stored in a mounted directory within the project

```bash
docker-compose up --build -d
```
