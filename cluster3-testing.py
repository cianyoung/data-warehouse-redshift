import boto3
from botocore.config import Config
import os
import configparser
import logging



config = configparser.ConfigParser()
config.read('dwh.cfg')

KEY = os.environ['AWS_ACCESS_KEY_ID']
SECRET = os.environ['AWS_SECRET_ACCESS_KEY']
REGION = config['CLUSTER']['REGION']

def create_resources():
    options = dict(region_name=REGION, aws_access_key_id=KEY, aws_secret_access_key=SECRET)
    ec2 = boto3.resource('ec2', **options)
    s3 = boto3.resource('s3', **options)
    iam = boto3.client('iam', **options)
    redshift = boto3.client('redshift', **options)
    return ec2, s3, iam, redshift

def check_clients(ec2, s3, iam, redshift):
    # check EC2 Client
    try:
        instances = [instance for instance in ec2.instances.all()]
        if len(instances) > 0:
            logging.info("EC2 client is working fine.")
        else:
            logging.info("EC2 client is created but no instances found.")
    except Exception as e:
        logging.info(f"EC2 client creation failed with error: {e}")
    # check S3 client
    try:
        buckets = [bucket for bucket in s3.bucket.all()]
        if len(buckets) > 0:
            logging.info("S3 client is working fine.")
        else:
            logging.info("S3 client is created but no buckets found.")
    except Exception as e:
        logging.info(f"S3 client creation failed with error: {e}")
    # Check IAM client
    try:
        response = iam.list_users()
        if response and response['Users']:
            logging.info("IAM client is working fine.")
        else:
            logging.info("IAM client is created but no users found.")
    except Exception as e:
        logging.info(f"IAM client creation failed with error: {e}")
    # Check Redshift client
    try:
        response = redshift.describe_clusters()
        if response and response['Clusters']:
            logging.info("Redshift client is working fine.")
        else:
            logging.info("Redshift client is created but no clusters found.")
    except Exception as e:
        logging.info(f"Redshift client creation failed with error: {e}")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(,essage)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
ec2, s3, iam, redshift = create_resources()
check_clients(ec2, s3, iam, redshift)