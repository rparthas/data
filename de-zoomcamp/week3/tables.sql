CREATE OR REPLACE EXTERNAL TABLE `dezoomcamp-341110.trips_data_all.green_taxi`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_dezoomcamp-341110/green/*.parquet']
);


CREATE OR REPLACE EXTERNAL TABLE `dezoomcamp-341110.trips_data_all.yellow_taxi`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_dezoomcamp-341110/yellow/*.parquet']
);