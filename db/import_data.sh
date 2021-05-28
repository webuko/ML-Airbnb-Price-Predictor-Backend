#!/bin/bash
mongoimport --host mongodb --port 27017 --db $1 --username $2 --password $3 --collection listings --drop --file /listings_seed_1.json --jsonArray
mongoimport --host mongodb --port 27017 --db $1 --username $2 --password $3 --collection listings --file /listings_seed_2.json --jsonArray

mongoimport --host mongodb --port 27017 --db $1 --username $2 --password $3 --collection neighbourhood_geo --file /geo_seed.geojson --jsonArray
