## DatCat
Simple data catalogue api.

###Convensions
Location: /datcat/schemas \
Filetype: .json \
Naming: your_schema_name_v1.json \
Platform: bigquery

###Format of a simple schema
```json
[
  {
    "description": "Unique Identifier",
    "mode": "REQUIRED",
    "name": "MY_UNIQUE_ID",
    "type": "INT64"
  },  {
    "description": "Favourite Colour",
    "mode": "REQUIRED",
    "name": "MY_FAVOURITE_COLOUR",
    "type": "STRING"
  }
]
```

### .env.example
```bash
#settings
SCHEMAS_PATH=/datcat/schemas
CATALOGUE_SCHEME=http
CATALOGUE_HOST=0.0.0.0
CATALOGUE_PORT=8080
CATALOGUE_DEBUG=False
PYTHONPATH=/datcat
```
### Build and run it inside a docker container example

```bash
source .env
poetry build --format wheel
docker build --tag dc .
docker run --hostname datcat \
  --env-file .env \
  --publish "${CATALOGUE_PORT}":"${CATALOGUE_PORT}" \
  --detach dc:latest
```

Now go to: http://0.0.0.0.8080 to see it