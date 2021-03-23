## DatCat
***
_Please note this is an alpha version and still in active development. Naturally all feedback is welcome._
***
Datcat is a simple and lightweight data catalogue api for big query.
Datcat loads your .json schema files to memory for use with either your own synchronisation service or [catasyn](https://github.com/antonio-one/catasyn) - it's sibling application.
Look into the example_catalogue directory or [here](https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file) to find out how to define your bigquery schemas.
Here's a quick snippet if you are as lazy as I am:

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

Currently, datcat supports partition generation and pii identification via tagging the relevant column's description with `{"partition": true}` and/or `{"pii": true}`.
```json
[
  ...
  ...
  ...
  {
    "description": "{\"pii\": true}",
    "mode": "REQUIRED",
    "name": "col_4",
    "type": "STRING"
  },
  {
    "description": "{\"partition\": true}",
    "mode": "REQUIRED",
    "name": "date",
    "type": "DATE"
  }
]
```

In addition to serving schema definitions via its api, it  creates a basic mapping between a schema - topic - subscriber that is later used to create the relevant infrastructure [[1]](footnote-1) from the schema definition.
After the schemas are defined run `python -m datcat.service_layer.mappings` to create those mappings. The naming conventions are basic, with each topic containing all versions of an event and each topic having only one subscriber for the purposes of data lake ingestion alone.

```json
//schema_topic_subscription.json
{
  "login_v1": {
    "schema_class_name": "login",
    "topic_name": "login_topic",
    "subscription_name": "login_subscription"
  },
  ...
  ...
  ...
```
CI/CD is your gig but if you fancy seeing datcat in action in your local docker run `./docker-docker-build.sh` and go to: http://0.0.0.0:50000

#### Footnote- 1
IAM and general permissions are out of scope in this project. It's up to you to ensure your service account has all the necessary roles/permissions to create bigquery tables and topics/subscribers. Check [this](https://cloud.google.com/iam/docs/understanding-roles) for a reminder.
