# data-warehouse-redshift

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

You are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights into what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Install
``` pip install requirements.txt ```

## Project Description

* Build an ETL pipeline for a database hosted on RedShift
* Load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables 

## Files

`create_cluster2.py`
* Create IAM role, Redshift cluster, and provision connectivity from outside VPC
* Pass `--delete` flag to delete resources

`create_tables.py`
* Drop and recreate tables

`dwh.cfg` 
* Configure Redshift cluster and data import

`etl.py`
* Copy data to staging tables and insert into star schema fact and dimension tables

`sql_queries2.py`

* Creating and dropping staging and star schema tables
* Copy JSON data from S3 to Redshift staging tables
* Insert data from staging tables to star schema fact and dimension tables 

## Run Scripts

* Set environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
* Set `DB` and `DB_PASSWORD` in config file, `dhw.cgh`
* Create Redshift cluster, IAM role, and configure network connectivity
``` $ python create_cluster.py ```
* Complete `dwh.cfg` with outputs from `create_cluster2.py`
** `CLUSTER / HOST`
** `IAM_ROLE / ARN`
* Drop and recreate tables
``` $ python create_tables.py ```
* Run ETL Pipeline
``` $ python etl.py ```
* Delete IAM role and Redshift cluster
``` $ python create_cluster2.py --delete ```
