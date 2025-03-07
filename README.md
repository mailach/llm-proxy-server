# Prompt Collection Bot

## App

The application that was used to collec the data.

### Development Setup

- run docker-compose dev setup, note that database will be rebuild for every restart

```bash
docker compose -f docker-compose-dev.yaml up
```

### Deployment Setup

- before first initialization add directory `data` 

```bash
docker compose up --build -d
```
