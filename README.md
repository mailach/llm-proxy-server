# LLM Proxy Server


### Development Setup

- run docker compose dev setup, note that database will be rebuild for every restart

```bash
docker compose -f docker-compose-dev.yaml up
```

### Deployment Setup

- before first initialization add directory `data`, this will be mapped in the database container and should be backed up regularly

```bash
docker compose up --build -d
```
