import boto3
from dostup import keys
from datetime import datetime, timezone
from    botocore.exceptions import ClientError
from    boto3.dynamodb.conditions import Key


session = boto3.session.Session()
TableName='temp_und_humid'

def write_bunches(client, massa):
    bunch_size = 25                                     # 25 - max bunch size
    cel = len(massa) // bunch_size           # количество полных банчей
    # записей в последнем, неполном, банче
    ostatok = len(massa) % bunch_size
    # количество полных банчей плюс последний огрызок
    for bunch_num in range(cel+1):
        # размер цикла =  bunch_size, если последний - то ostatok, который может быть и 0
        cycles = bunch_size if (bunch_num != cel) else ostatok
        # инициализация списка текучего банча
        bunch = []
        for i in range(cycles):
            # numb - индекс записи в общем списке
            numb = bunch_size * bunch_num + i
            # one Temperature Humidity record
            th_record = massa[numb]
            item_dict = {
                "device_id":   {"S": th_record["device_id"]}, # if boto3.RESOURCE : key attribute - no type specify, just value
                "date":        {"S": th_record["date"]},
                "temperature": {"N": th_record["temperature"]},
                "humidity":    {"N": th_record["humidity"]},
            }
            record_putts = {"PutRequest": {"Item": item_dict}}
            bunch.append(record_putts)
        response = 77
        try:
            response = client.batch_write_item(RequestItems={TableName: bunch})
            print(f">>>>>>>>>>>>> {bunch}  <<<<<<<<<<<<<<response<< {response} <<<<<<<<<<<<<<<")
        except Exception as erro:
            return f"\tException '{erro}' occured\n\ttype '{type(erro)}'"

            print(f">EOORRRRRRR {bunch}  <<<  response >> {response}  <<<<<<<<<<<<<<<<<<<<<<<")
    return (0)


def scan_all_table(client):
    table = client.Table(TableName)
    response = table.scan()  # scan without conditions
    ret = response['Items']
    return ret

def cleartable(client):
    regcovidstat = scan_all_table(document_api_endpoint)
    bunch_size = 25
    cel     = len(regcovidstat) // bunch_size
    ostatok = len(regcovidstat) %  bunch_size

    for bunch_num in range(cel+1):
        cycles = bunch_size if (bunch_num != cel) else ostatok
        bunch = []
        for i in range(cycles):
            numb = bunch_size * bunch_num + i
            daystat = regcovidstat[numb]
            item_dict = {
                "device_id": daystat["device_id"] ,
            }
            dayputts = {"DeleteRequest" : {"Key" : item_dict}}
            bunch.append(dayputts)
        try:
            response = client.batch_write_item(
                RequestItems={ TableName: bunch }
            )
        except Exception as erro:
            exc = f"\tException '{erro}' occured\n\ttype '{type(erro)}'"
            print(exc)
            return (exc)

    return (0)

ydb_client = session.client(
    service_name        =   'dynamodb',
    endpoint_url        =   keys['document_api_endpoint'],
    aws_access_key_id   =   keys['aws_access_key_id'],
    aws_secret_access_key=  keys['aws_secret_access_key'],
    region_name         =   keys['region_name'],
)

rec = {
    "device_id": "devid",
    "date": "dattas",
    "temperature": "20.02",
    "humidity": "55.55",
}
ret = cleartable(ydb_client) ;
#ret = write_bunches(ydb_client, [rec])
print (ret)
""""
a = ydb_client.put_item(
    TableName='temp_und_humid',
    Item={'device_id': {'S': 'arelgtlkga1icc1cvoqm'},
         'date' : {'S': '2023-04-12 16:56:18'},
          'some' : {'N': '77.777'},
         })
print(a)
"""

exit(0)


