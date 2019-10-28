import egnyte
import datetime
import requests
import json
import datetime
import os

# client = egnyte.EgnyteClient({"domain": "rheosrx.egnyte.com",
#     "access_token": ""})
#
# api = egnyte.base.HasClient
#
# folder = client.folder("/Private/vqin")
#
# folder.list()
#
# results = client.search.files('test_file_2.csv', folder='/Private/vqin')
#
# resultsreal = client.SearchMatch(results)
#
# print(resultsreal)
# time = datetime.datetime.now() - datetime.timedelta(days=60)
#
# time_real = time.isoformat()
# print(time_real)
# url = 'http://rheosrx.egnyte.com/pubapi/v1/search?query=*.txt&modified_after='+ time_real
#
# auth = 's2mkz4nxr496h8stnk5dar9z'
#
# headers = {"Authorization":"Bearer s2mkz4nxr496h8stnk5dar9z" }
#
# resp = requests.get(url, headers = headers)
#
# output = json.loads(resp.content)
# print(output)
# print(type(output))
# print(output.get("results")[0].get("path"))
# with open('output.txt','w') as f:
#     results = output.get("results")
#     counter = 1
#     for line in results:
#         if counter != len(results):
#             path = results[counter].get("path")
#             print >> f,path
#             counter +=1

home = os.path.expanduser('~')
if not os.path.exists(home + '/Rheosrx'):
    print('exists')

year = datetime.date.today().year

month = datetime.date.today().month

if len(str(month)) != 2:
    real_month = str('0') + str(month)
else:
    real_month = month

print(str(year)+'-' + str(real_month))