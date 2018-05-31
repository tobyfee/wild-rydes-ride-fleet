'''Test get_unicorn'''
# pylint: disable=protected-access
# pylint: disable=wrong-import-position
# pylint: disable=redefined-outer-name
import os

import boto3
from moto import mock_dynamodb2, mock_sts

# Need to ensure function environment settings are set before import
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE'] = 'mock_test_request_ride'
DYNAMODB_HASH_KEY = os.environ['UNICORN_HASH_KEY'] = 'Name'
import handlers.get_unicorn as h # noqa


@mock_sts   # Let's us handle assumed roles.
@mock_dynamodb2
def test__get_unicorn():
    '''Test recording a ride'''
    ddb = boto3.client('dynamodb')
    ddb.create_table(
        TableName=DYNAMODB_TABLE,
        KeySchema=[
            {
                'AttributeName': DYNAMODB_HASH_KEY,
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[{'AttributeName': DYNAMODB_HASH_KEY,
                               'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1,
                               'WriteCapacityUnits': 1}
    )

    unicorn = {"Name": "Mock", "Color": "Green"}
    ddb_res = boto3.resource('dynamodb')
    ddt = ddb_res.Table(DYNAMODB_TABLE)
    ddt.put_item(
        TableName=DYNAMODB_TABLE,
        Item=unicorn
    )

    this_unicorn = h._get_unicorn()
    assert this_unicorn.get('Name') == unicorn.get('Name')
    assert this_unicorn.get('Color') == unicorn.get('Color')

