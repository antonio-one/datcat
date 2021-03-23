#!/bin/bash

source .env

docker rmi "$(docker images --filter dangling=true -q)" 2> /dev/null
docker container prune --force 2> /dev/null
rm dist/datcat* 2> /dev/null

CONTAINER_NAME=datcat
docker rm -f ${CONTAINER_NAME} 2>/dev/null

poetry build --format wheel
docker build --tag ${CONTAINER_NAME} .

CONTAINER_HOSTNAME="datcat_"$(uuidgen | awk -F- '{print $1}')
echo "CONTAINER_HOSTNAME=${CONTAINER_HOSTNAME}"

CONTAINER_ID=$(
docker run --hostname "${CONTAINER_HOSTNAME}" \
  --name datcat \
  --env-file .env \
  --publish 50000:"${CATALOGUE_PORT}" \
  --detach ${CONTAINER_NAME}
  )

echo "[STOP COMMAND COPIED TO CLIPBOARD] docker stop ${CONTAINER_ID}"
echo "docker stop ${CONTAINER_ID}" | pbcopy

docker exec -it "${CONTAINER_ID}" /bin/bash
