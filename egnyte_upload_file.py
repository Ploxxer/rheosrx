import requests
import simplejson
import egnyte

# client = egnyte.EgnyteClient({"domain": "apidemo.egnyte.com",
#     "access_token": ""})
#
# folder = client.folder("/Private/vqin/hello").create()


url = 'https://rheosrx.egnyte.com/pubapi/v1/fs/Private/vqin'

headers = {"Authorization":"Bearer " }

egnyte_data = {"action": "add_folder"}

resp = requests.post(url, headers = headers, data = egnyte_data)

print(resp.status_code)
print(resp.content)