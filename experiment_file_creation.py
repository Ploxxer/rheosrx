import requests
import simplejson
import datetime
import os

get_url = 'https://node-25.exemplareln.com:8443/velox_webservice/api/datarecord?datatype=ELNExperiment'
auth = ('' , '')
headers = {'guid':''}

resp = requests.get(get_url, auth = auth , headers = headers)

content = simplejson.loads(resp.content)

print(len(content))

with open('instrument_name.txt', 'r') as f:
    name = f.readline()

year = datetime.date.today().year

month = datetime.date.today().month

if len(str(month)) != 2:
    real_month = str('0') + str(month)
else:
    real_month = month

time = str(year)+'-' + str(real_month)

datenow = datetime.datetime.now()

for line in content:
    datecreated= line['fields']['DateCreated']
    date = datetime.datetime.fromtimestamp(datecreated / 1e3)

    datediff = datenow - date

    if datediff.total_seconds() < 7 * 24 * 3600:

        print(datediff)
        num1 = line['fields']['RelatedNotebookExperiment']

        get_url2 = 'https://node-25.exemplareln.com:8443/velox_webservice/api/datarecord?datatype=ELNExperimentDetail&field=RelatedNotebookExperiment&values=' + str(num1)

        resp2 = requests.get(get_url2, auth=auth, headers=headers)

        content2 = simplejson.loads(resp2.content)

        for line2 in content2:
            instrument_used = (line2['fields'].get('InstrumentUsed'))
            instrument_type = (line2['fields'].get('InstrumentType'))
            experiment_name = (line['fields']['DataRecordName'])
            if instrument_used == name:
                print(instrument_type)
                print(instrument_used)
                # get_url3 = 'https://node-25.exemplareln.com:8443/velox_webservice/api/datarecord?datatype=Instrument&field=InstrumentName&values=' + str(instrument_used)
                # resp3 = requests.get(get_url3, auth=auth, headers=headers)
                # content3 = simplejson.loads(resp3.content)
                #
                # print(content3)
                # instrument_path = content3[0]['fields'].get('NetworkFilePath')
                # print('this is the path')
                # print(instrument_path)

                #once on local machine, create textfile containing name of the machine it is one
                #if text is the same as instrument_type and/or instrument_used, execute the creation of folder structures
                #else ignore creation


                egnyte_url = 'https://rheosrx.egnyte.com/pubapi/v1/fs/Private/vqin/LAB-DATA/' + str(instrument_type) + '/' + str(instrument_used) + '/' + time + '/' + str(experiment_name)

                egnyte_headers = {"Authorization": "Bearer s2mkz4nxr496h8stnk5dar9z"}

                egnyte_data = {"action": "add_folder"}

                resp3 = requests.post(egnyte_url, headers=egnyte_headers, json=egnyte_data)

                status = resp3.status_code

                print(status)

                if status == 201:
                    print('new folder created')
                elif status == 403:
                    print('folder already exists')
                else:
                    print('something went wrong')

                home = os.path.expanduser('~')

                if os.path.exists(home + '/LAB-DATA/' + str(instrument_type) + '/' + str(instrument_used) + '/' + time + '/' + str(experiment_name)):
                    print('local dir already exists')
                else:
                    os.makedirs(home + '/LAB-DATA/' + str(instrument_type) + '/' + str(instrument_used) + '/' + time + '/' + str(experiment_name))
                    print('local dir created')

                print(line['fields']['DataRecordName'])
                print(line['fields']['RecordId'])

