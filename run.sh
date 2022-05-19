#!/bin/bash
echo "To enter into the database execute the following command: psql -h localhost -p 5432 -d formula1_db -U admin"
sudo docker rm -f postgresql_database, create_tables_sh, load_data_py
sudo docker-compose up