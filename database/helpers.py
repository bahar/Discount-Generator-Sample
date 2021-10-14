import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def insert_items_in_btach(table_name=None, items=None, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

	table = dynamodb.Table(table_name)

	try:
		with table.batch_writer() as batch:
			for item in items:
				batch.put_item(Item=item)
		return True
	except Exception as e:
		print(str(e))
		return False

def find_user(user_id=None, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
	users_table = dynamodb.Table("Users")

	response = users_table.query(
		KeyConditionExpression=Key('user_id').eq(user_id)
	)
	if response["Count"] >0:
		return response['Items'][0]
	else:
		return None

def get_unused_discount_code(user_id=None, brand_id=None, dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
	discounts_table = dynamodb.Table("Discounts")

	response = discounts_table.scan(FilterExpression = Attr('brand_id').eq(brand_id))

	if(response['Count'] == 0):
	 return '' #No disount is available for this brand

	discount_code = response['Items'][0]["code"]
	brand_id = response['Items'][0]["brand_id"]

	used_code_table = dynamodb.Table("Used_Codes")

	try:
		response = discounts_table.delete_item(
		    Key={
		        'code': discount_code,
		        'brand_id': brand_id
		    }
		)
	except ClientError as e:
	    if e.response['Error']['Code'] == "ConditionalCheckFailedException":
	        print(e.response['Error']['Message'])
	    else:
	        raise
	else:
		used_code_table.put_item(
			Item={
	            'code': discount_code,
	            'user_id': user_id,
	        }
		)

		return discount_code



