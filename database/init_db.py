import boto3
from botocore.exceptions import ClientError

def if_table_exists(dynamodb=None, table=None):
    try:
      is_table_existing = table.table_status in ("CREATING", "UPDATING",
                                                 "DELETING", "ACTIVE")
    except ClientError:
      is_table_existing = False
    return is_table_existing

def create_discounts_table(dynamodb=None):
    table_name = "Discounts"
    table = dynamodb.Table(table_name)
    if(if_table_exists(dynamodb, table)):
        table.delete()
    table = dynamodb.create_table(
        TableName='Discounts',
        KeySchema=[
            {
                'AttributeName': 'code',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'brand_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'code',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'brand_id',
                'AttributeType': 'N'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

def create_used_codes_table(dynamodb=None):
    table_name = "Used_Codes"
    table = dynamodb.Table(table_name)
    if(if_table_exists(dynamodb, table)):
        table.delete()

    table = dynamodb.create_table(
        TableName='Used_Codes',
        KeySchema=[
            {
                'AttributeName': 'code',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'user_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'code',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'user_id',
                'AttributeType': 'N'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

def create_user_table(dynamodb=None):
    table_name = "Users"
    table = dynamodb.Table(table_name)
    if(if_table_exists(dynamodb, table)):
        table.delete()

    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'user_email',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'user_email',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    #initialize with sample user, which we will be using for this demo
    table.put_item(
       Item={
            'user_id': 2341,
            'user_name': 'Habib Ullah Bahar',
            'user_email': 'iambahar@gmail.com',
            'user_mobile': '+46739559098',
            'user_secret': 'jhjdvbfehfbu468hGFVYUGHBIUIUYRD' 
        }
    )

    return table

if __name__ == '__main__':

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    discounts_table = create_discounts_table(dynamodb)
    used_codes = create_used_codes_table(dynamodb)
    users_table = create_user_table(dynamodb)
    print("Table status: \n Discounts: %s \n Used_Codes: %s \n Users: %s" % (discounts_table.table_status, used_codes.table_status, users_table.table_status))



