import argparse
import logging
import configparser

config = configparser.ConfigParser()
config.read('dwh.cfg')

KEY = os.environ['AWS_ACCESS_KEY_ID']
SECRET = os.environ['AWS_SECRET_ACCESS_KEY']
REGION = config['CLUSTER']['REGION']

DWH_CLUSTER_ID = config['CLUSTER']['DWH_CLUSTER_IDENTIFIER']


def create_resources():
    options = dict(region_name=REGION, aws_access_key_id=KEY, aws_secret_access_key=SECRET)
    ec2 = boto3.resource('ec2', **options)
    s3 = boto3.resource('s3', **options)
    iam = boto3.client('iam', **options)
    redshift = boto3.client('redshift', **options)
    return ec2, s3, iam, redshift


def delete_redshift_cluster(redshift):
    """ Delete redshift cluster """
    try:
        redshift.delete_cluster(
            ClusterIdentifier=DWH_CLUSTER_ID,
            SkipFinalClusterSnapshot=True,
        )
        logging.info('Deleted cluster {}'.format(DWH_CLUSTER_ID))
    except Exception as e:
        logging.error(e)


def delete_iam_role(iam):
    """ Delete IAM role """
    try:
        role_arn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']
        iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn=S3_READ_ARN)
        iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
        logging.info('Deleted role {} with {}'.format(DWH_IAM_ROLE_NAME, role_arn))

    except Exception as e:
        logging.error(e)

def create_iam_role(iam):
    """ Create an IAM role """
    try:
        dwh_role = iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps({
                'Statement': [{
                        'Action': 'sts:AssumeRole',
                        'Effect': 'Allow',
                        'Principal': {'Service': 'redshift.amazonaws.com'}
                }],
                    'Version': '2012-10-17'
                })
            )
        iam.attach_role_policy(
            RoleName=DWH_IAM_ROLE_NAME,
            PolicyArn=S3_READ_ARN
        )
    except ClientError as e:
        logging.warning(e)

def create_redshift_cluster(redshift, role_arn):
    """ Create Redshift cluster """
    try:
        redshift.create_cluster(
            ClusterType=config['CLUSTER']['DWH_CLUSTER_TYPE'],
            NodeType=config['CLUSTER']['DWH_NODE_TYPE'],
            NumberOfNodes=int(config['CLUSTER']['DWH_NUM_NODES']),
            DBName=config['DB']['DB_NAME'],
            ClusterIdentifier=DWH_CLUSTER_ID,
            MasterUsername=config['DB']['DB_USER'],
            MasterUserPassword=config['DB']['DB_PASSWORD'],
            IamRoles=[role_arn],
        )
        logging.info('Creating cluster {}...'.format(DWH_CLUSTER_ID))
    except ClientError as e:
        logging.warning(e)


def main(args):
    """ Main Function """
    logging.info('Entering the main function ...')
    # create clientsla

    ec2, s3, iam, redshift = create_resources()
    if args.delete:
        delete_redshift_cluster(redshift)
        delete_iam_role(iam)
    else:
        role_arn = create_iam_role(iam)
        create_redshift_cluster(redshift, role_arn)

        """ Poll cluster after creation to check availability """



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(,essage)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Starting...')
    """ Set logging and CLI arguments """
    # Create an instance of the parser class and store in parser variable
    parser = argparse.ArgumentParser()
    parser.add_argument('--delete', dest='delete', default=False, action='store_true')
    args = parser.parse_args()
    main(args)
