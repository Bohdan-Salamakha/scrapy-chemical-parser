### Environment variables
### Create .env file in the root directory using .env_sample template.

### Endpoint for average value
### [GET] /parsers/get-average-price-per-unit/?numcas=<STRING>

#### For examples:
#### [GET] ```/parsers/get-average-price-per-unit/?numcas=1186657-97-5```
#### Will return ```{"average": 861.8 }```
### Spider start
### ```curl http://localhost:6800/schedule.json -d project=default -d spider=accelpharmtech_spider```