import  json

s = "https://docapi.serverless.yandexcloud.net/ru-central1/b1gatc4m3hv1ldldhljp/etnp3f35ot2jos2cgtt7"


ff = s[s.find("yandexcloud.net/")+len("yandexcloud.net/")-1:]

print(ff)

event = '{"series_id": 2024}'

dmp = json.dumps(event)
w2g = json.loads(event)
w = json.loads(dmp)
dm = json.dumps(w)
b = 0