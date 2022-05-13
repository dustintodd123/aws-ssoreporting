import json
import os
import time
import getopt
import csv
import sys
import requests


infile, outfile = None, None
argumentList = sys.argv[1:]
try:
    opts, args = getopt.getopt(argumentList, "infile:outfile:colname", ["infile=", "outfile=","colname="])
except getopt.GetoptError:
    print('aws-ssoreporting.py --infile <emails_file> --outfile <report_file> --colname <csv_column_header_name')
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print('aws-ssoreporting.py --infile <emails_file> --outfile <report> --colname <csv_column_header_name')
        sys.exit()
    elif opt in ("-infile", "--infile"):
        infile = arg
        print('Email file' + infile)
    elif opt in ("-outfile", "--outfile"):
        outfile = arg
        print('Report file' + outfile)
    elif opt in ("-colname", "--colname"):
        emailHeader = arg
        print('Email column name ' + emailHeader)

# AWS SCIM Token
auth_token = os.environ.get('SCIMTOKEN')
# AWS SCIM url - acct specific
url = os.environ.get('URL')
# Setup requests header
headers = {'Authorization': 'Bearer {}'.format(auth_token)}
print(headers)

# Setup report writer
rpt_file = open(outfile, "w")
rpt_file.truncate()
writer = csv.writer(rpt_file,delimiter=',')

# Setup CSV email addr file
filename = open(infile, 'r')
emailsCsv = csv.DictReader(filename)
emails = {}
# Read each email address and query to get ID from AWS
for col in emailsCsv:

    response = requests.get(url + '/Users', headers=headers, params={'filter': 'userName eq "' +
                                                                                   col[emailHeader] + '"'})
    if response.status_code == 200:
        scimUser = json.loads(response.text)
        if scimUser['totalResults'] > 0:
            emails[col[emailHeader]] = []
            emails[col[emailHeader]].append({'id': scimUser['Resources'][0]['id'],
                                             'name': scimUser['Resources'][0]['name']})
        else:
            print('Email not in SSO store: ' + col['Email Address [Required]'])
    else:
        print('SCIM user request failed: ' + response.headers['x-amzn-ErrorType'])
    # Don't get rated limited
    time.sleep(.1)

print('email file load complete - Found:', len(emails))
# print(emails)

# Get all SSO groups
response = requests.get(url + '/Groups', headers=headers)
if 200 != response.status_code:
    print('SCIM List groups error: ' + response.headers['x-amzn-ErrorType'])
    exit(2)
else:
    groups = json.loads(response.text)

# Iterate through each group
for groups in groups['Resources']:
    print('Groupname: ' + groups['displayName'])
    # for each email address and group perform group check
    # Why AWS thinks this is an ok solution is beyond explanation
    for key, value in emails.items():
        response = requests.get(url + '/Groups', headers=headers, params={
            'filter': 'id eq "' + groups['id'] + '" and members eq "' + value[0]['id'] + '"'})
        if response.status_code == 200:
            groupData = json.loads(response.text)
            if groupData['totalResults'] > 0:
                writer.writerow([key, value[0]['name']['givenName'], value[0]['name']['familyName'], groupData['Resources'][0]['displayName']])
                print(groupData['Resources'][0]['displayName'] + ' ' + key)
        else:
            print('SCIM request failed: ' + response.headers['x-amzn-ErrorType'])

rpt_file.close()