import requests
import simplejson

# url = 'https://node-25.exemplareln.com:8443/velox_webservice/api/datarecord?datatype=ELNExperimentDetail&field=RelatedNotebookExperiment&values=7509'
url = 'https://node-25.exemplareln.com:8443/velox_webservice/api/report/system?report=Experiments Using Instruments'

auth = ('' , '')
headers = {'guid':''}

resp = requests.get(url, auth = auth , headers = headers)

if resp.status_code == 200:
    print("connection is good")

content = simplejson.loads(resp.content)

print(len(content))
print(content)

output = resp.content.split(',')

with open('report.txt','w') as f:
    real_content = content.get('results')
    for line in real_content:
        print(line[0])
        print(line[4])

        print >> f , line

