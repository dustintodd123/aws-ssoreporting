import os
import json
import requests

# AWS SCIM Token
auth_token = os.environ.get('SCIMTOKEN')
# AWS SCIM url - acct specific
url = os.environ.get('URL')
headers = {'Authorization': 'Bearer {}'.format(auth_token)}

response = requests.get(url + '/Users', headers=headers)

print(response.status_code)
print(response.url)
print(response.headers)
content = json.loads(response.text)
for users in content['Resources']:
    print(users['id'] + " " + users['userName'])

print("Status Code", response.status_code)
print(content['totalResults'])
print(content['itemsPerPage'])