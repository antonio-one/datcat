## DatCat
Simple data catalogue api for big query.
Please note this is an alpha version and still in active development.

### Convensions
Location: datcat/catalogue/schemas \
Filetype: .json \
Naming: your_schema_name_v1.json \

### Format of a Simple Schema
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

### Table options
You may use {"partition": true} and/or {"pii": true} in the column description.


### Run Datcat
#### With Docker
```bash
./docker-docker-build.sh
```
Go to: http://0.0.0.0:50000 to see it
#### With uvicorn directly
```bash
uvicorn datcat.entrypoints.app:app --host 0.0.0.0 --port 80
````

### Test Coverage
```bash
cd tests
pytest -vv --cov=. | grep -v .env
```
