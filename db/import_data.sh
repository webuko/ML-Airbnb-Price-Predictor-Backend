#!/bin/bash
mongoimport --host mongodb --port 27017 --db $1 --username $2 --password $3 --collection listings --file /seed_data_1.json --jsonArray
mongoimport --host mongodb --port 27017 --db $1 --username $2 --password $3 --collection listings --file /seed_data_2.json --jsonArray