#!/bin/bash
echo "To enter into the database execute the following command: psql -h localhost -p 5432 -d formula1_db -U admin"
sudo docker-compose rm -f
sudo docker-compose up