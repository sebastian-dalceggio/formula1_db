#!/bin/bash
sudo docker rm -f postgresql_database
sudo docker-compose up
echo "To enter into the database execute the following command: psql -h localhost -p 5432 -d formula1_db -U admin"