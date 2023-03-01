import boto3
from dostup import keys

session = boto3.session.Session()
s3 = session.client(
    service_name        =   's3',
    endpoint_url        =   keys['endpoint_url'],
    aws_access_key_id   =   keys['aws_access_key_id'],
    aws_secret_access_key=  keys['aws_secret_access_key'],
    region_name         =   keys['region_name'],
)

response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

#s3.create_bucket(Bucket='pezdol')

a = 4