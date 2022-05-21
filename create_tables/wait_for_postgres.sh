#!/bin/bash

until psql postgresql://$USER:$PASSWORD@$HOST/$DATABASE  -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
  
echo "Postgres is up - executing command"
exec "$@"