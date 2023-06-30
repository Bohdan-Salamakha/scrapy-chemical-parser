### 1
### ```docker-compose up --build -d```
### 2
### Create .env file in the root directory using .env_sample template.
### 3
### Start the spider
### ```curl http://localhost:6800/schedule.json -d project=default -d spider=accelpharmtech_spider```
### 4
### Endpoint for average value
### [GET] /parsers/get-average-price-per-unit/?numcas=<...>
#### For examples:
#### [GET] ```/parsers/get-average-price-per-unit/?numcas=1186657-97-5```
#### Will return ```{"average": 861.8 }```