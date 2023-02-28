import boto3
#session = boto3.Session(
 #   aws_access_key_id="YCAJEBNOC7Mz-EgRUVQttMlMg",
  #  aws_secret_access_key="YCPOR7mHNrPbBC2bljJTN6AJj9KQQtIvLSLAvtw9",
   # region_name= "ru-central1",
#    endpoint_url='https://storage.yandexcloud.net'
#)

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id="YCAJEBNOC7Mz-EgRUVQttMlMg",
    aws_secret_access_key="YCPOR7mHNrPbBC2bljJTN6AJj9KQQtIvLSLAvtw9",
    region_name="ru-central1",

)

response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

#s3.create_bucket(Bucket='pezdol')

a = 4