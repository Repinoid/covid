import boto3
from dostup import keys
from datetime import datetime, timezone

timestamp = 1681145778

ti = datetime.fromtimestamp(timestamp)

t = ti.strftime('%Y-%m-%d %H:%M:%S')

#dynamodb = boto3.resource('dynamodb', endpoint_url=keys['document_api_endpoint'])

session = boto3.session.Session()
ydb_client = session.client(
    service_name        =   'dynamodb',
    endpoint_url        =   keys['document_api_endpoint'],
    aws_access_key_id   =   keys['aws_access_key_id'],
    aws_secret_access_key=  keys['aws_secret_access_key'],
    region_name         =   keys['region_name'],
)

a = ydb_client.put_item(
    TableName='temp_und_humid',

    Item={'device_id': {'S': 'arelgtlkga1icc1cvoqm'},
         'date' : {'S': '2023-04-12 16:56:18'},
          'some' : {'N': '77.777'},
         })
print(a)

exit(0)

