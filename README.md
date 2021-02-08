## DatCat
Simple data catalogue api.
Please note this is an alpha version and still in active development.

###Convensions
Location: datcat/catalogue/schemas \
Filetype: .json \
Naming: your_schema_name_v1.json \
Platform: bigquery

###Format of a Simple Schema
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
SCHEMAS_PATH=catalogue/schemas
METADATA_PATH=catalogue/metadata
MAPPINGS_FILEPATH=catalogue/mappings/schema_topic_subscription.json

CATALOGUE_SCHEME=http
CATALOGUE_HOST=0.0.0.0
CATALOGUE_PORT=50000
CATALOGUE_DEBUG=False
```
### Build and Run it Inside a Docker Container Example
Some useful code perhaps.
```bash
source .env

# cleanup
docker rmi "$(docker images --filter dangling=true -q)" 2> /dev/null
docker container prune --force 2> /dev/null
rm dist/datcat* 2> /dev/null

# build your container
poetry build --format wheel
docker build --tag datcat .

# make a hostname for fun
CONTAINER_HOSTNAME="datcat_"$(uuidgen | awk -F- "{print $1}")
echo "CONTAINER_HOSTNAME=${CONTAINER_HOSTNAME}"

# run it
CONTAINER_ID=$(
docker run --hostname "${CONTAINER_HOSTNAME}" \
  --name datcat \
  --env-file .env \
  --publish 50000:"${CATALOGUE_PORT}" \
  --detach datcat
  )

# copy the stop command to clipboard for convenience
echo "docker stop ${CONTAINER_ID}" | pbcopy

# container cli
docker exec -it "${CONTAINER_ID}" /bin/bash
```

Now go to: http://0.0.0.0:50000 to see it

### Test Coverage
```bash
cd tests
pytest -vv --cov=. | grep -v .env
```
