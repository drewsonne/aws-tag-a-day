from boto3 import Session
from botocore.exceptions import ClientError

from tag_a_day.cache import AWSCache
from tag_a_day.config import Configuration
from tag_a_day.log import logger
from tag_a_day.services import Services


def _initialise_common():
    def aws_session(region='us-east-1'):
        return Session(region_name=region)

    conf = Configuration(aws_session).parse()
    return aws_session, conf


def run():
    aws_session, conf = _initialise_common()
    cache = AWSCache(aws_session)

    table = aws_session(). \
        resource('dynamodb', conf.dynamodb_table_region). \
        Table(conf.dynamodb_table_name)
    services = Services(
        session=aws_session,
        cache=cache,
        services=conf.services,
        proposals=table)

    for region in conf.regions:
        session = aws_session(region)
        for service in services:
            logger().info(
                'Auditing tags for {0} in {1}'.format(service, region))
            service.run(
                expected_tags=conf.required_tags,
                region=region,
                session=session
            )


def initialise():
    aws_session, conf = _initialise_common()
    table_region = conf.dynamodb_table_region
    table_name = conf.dynamodb_table_name

    dynamodb = aws_session(table_region).client('dynamodb')
    print("Checking if table exists...")
    foundTable = True
    try:
        dynamodb.describe_table(TableName=table_name)
    except ClientError as e:
        if e.response.get('Error') == 'ValidationException':
            foundTable = False

    if foundTable:
        print("Table '{table_name}' already exists.".format(table_name=table_name))


if __name__ == '__main__':
    run()
