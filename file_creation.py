#!/usr/bin/env python2

import requests
import simplejson
import datetime
import os
import time
import logging
import shutil

#do prerequisite stuff like starting logger, getting list of experiments, the egnyte_path, getting date format

logging.basicConfig(
    filename="test.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

get_url = 'https://a4633.exemplareln.com/velox_webservice/api/datarecord?datatype=ELNExperiment'
auth = ('' , '')
headers = {'guid':''}

resp = requests.get(get_url, auth = auth , headers = headers)

content = simplejson.loads(resp.content)

client_url = 'https://a4633.exemplareln.com/velox_webservice/api/datarecord?datatype=ClientConfigurations'

resp4 = requests.get(client_url, auth = auth , headers = headers)

content4 = simplejson.loads(resp4.content)

egnyte_path = content4[0]['fields'].get('EgnyteFTPRootPath')

logging.debug("EgnyteFTPRootPath: " + egnyte_path)

with open('instrument_name.txt', 'r') as f:
    #text in file should match name of instrument
    name = f.readline()
    print(name)

year = datetime.date.today().year

month = datetime.date.today().month

if len(str(month)) != 2:
    real_month = str('0') + str(month)
else:
    real_month = month

formatted_date = str(year)+'-' + str(real_month)

datenow = datetime.datetime.now()

for line in content:

    #get date differences so that only experiments created within the time frame are considered

    datecreated= line['fields']['DateCreated']
    date = datetime.datetime.fromtimestamp(datecreated / 1e3)

    datediff = datenow - date

    if datediff.total_seconds() < 5 * 24 * 3600:

        #use RelatedNotebookExperiment within experiments to point towards ELNExperimentDetail where instrument data is stored

        print(datediff)
        num1 = line['fields']['RelatedNotebookExperiment']

        get_url2 = 'https://a4633.exemplareln.com/velox_webservice/api/datarecord?datatype=ELNExperimentDetail&field=RelatedNotebookExperiment&values=' + str(num1)

        resp2 = requests.get(get_url2, auth=auth, headers=headers)

        content2 = simplejson.loads(resp2.content)
        print(content2)
        for line2 in content2:
            instrument_used = (line2['fields'].get('InstrumentUsed'))
            instrument_type = (line2['fields'].get('InstrumentType'))
            experiment_name = (line['fields']['DataRecordName'])
            if instrument_used == name:

                print(instrument_type)
                print(instrument_used)

                #name variable will change depending on the instrument the instrument_name.txt file is on
                #ie. Countess01 , Biotek-1
                #since this program will be constantly running on every machine, every local machine will only have the experiments
                #that contain the instrument being used while egnyte will have all experiements within the /Shared/Lab Data/Sapio Sandbox folder
                #since each local machine is writing to egnyte

                #does a bunch of path stuff to get final paths for egnyte and local machine
                #dependent of stuff set in console like workstationid, automatedsubfolderlist, localdriveletter etc.

                get_url3 = 'https://a4633.exemplareln.com/velox_webservice/api/datarecord?datatype=Instrument&field=InstrumentName&values=' + str(name)
                resp3 = requests.get(get_url3, auth=auth, headers=headers)
                content3 = simplejson.loads(resp3.content)

                print(content3)
                instrument_path = content3[0]['fields'].get('WorkstationId')
                print('this is the path')
                print(instrument_path)

                sub_folders = content3[0]['fields'].get('AutomatedSubfolderList')
                print(sub_folders)

                sub_folder_list = sub_folders.split(',')

                drive_letter = content3[0]['fields'].get('LocalDriveLetter')

                print(drive_letter)

                network_path = content3[0]['fields'].get('NetworkFilePath')

                print(network_path)

                new_path = network_path.replace('{InstrumentType}' , instrument_type)
                new_path1 = new_path.replace('{InstrumentName}' , instrument_used)
                new_path2 = new_path1.replace('{Date(YYYY-MM)}' , formatted_date)
                new_path3 = new_path2.replace('{ExpName}' , experiment_name)
                new_path4 = new_path3.replace('/' , '\\')

                print(new_path4)
                egnyte_url_path = egnyte_path + new_path3

                print(egnyte_url_path)
                logging.debug(egnyte_url_path)

                local_path = drive_letter + instrument_path + '\\'+ new_path4

                print(local_path)
                logging.debug(local_path)

                egnyte_url = 'https://rheosrx.egnyte.com/pubapi/v1/fs/Private/vqin' + str(egnyte_url_path)

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

                if os.path.exists(home + '/LAB-DATA/' + str(instrument_type) + '/' + str(instrument_used) + '/' + formatted_date + '/' + str(experiment_name)):
                    print('local dir already exists')
                else:
                    os.makedirs(home + '/LAB-DATA/' + str(instrument_type) + '/' + str(instrument_used) + '/' + formatted_date + '/' + str(experiment_name))
                    for folder in sub_folder_list:
                        print('start ' + str(folder))
                        resp5 = requests.post(egnyte_url + '/' + str(folder), headers=egnyte_headers, json=egnyte_data)
                        time.sleep(.5)
                        print(resp5.status_code)
                        print('egnyte subfolder created '+ str(folder))

                        os.makedirs(home + '/LAB-DATA/' + str(instrument_type) + '/' + str(instrument_used) + '/' + formatted_date + '/' + str(experiment_name) + '/' + str(folder))
                        print('local subfolder created ' + str(folder))
                        print('')

                    print('local dir created')

                print(line['fields']['DataRecordName'])
                print(line['fields']['RecordId'])

logging.info("")

time.sleep(.5)

#if the size of the log file is greater than the specified size, copy the log file with appended current date into log_folder and delete the log file
#if there are more than 3 files within log_folder, delete the oldest log file

statfile = os.stat('test.log')
size = statfile.st_size
if size > 10000:
    if os.path.exists('./test.log'):
        path = os.path.abspath('test.log')
        shutil.copy(path , '/Users/qin_vern/Rheosrx/egnyte_development/log_folder/test-'+ str(datenow) + '.log')
        os.remove('./test.log')

    dir_num = os.listdir('./log_folder')

    if len(dir_num) > 3:
        path = './log_folder'
        os.chdir(path)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getctime)

        oldest = files[0]
        os.remove(oldest)

