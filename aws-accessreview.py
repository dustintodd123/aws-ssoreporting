import json
import os
import time
import getopt
import csv
import sys
import requests
from datetime import date

infile, outfile = None, None
argumentList = sys.argv[1:]
try:
    opts, args = getopt.getopt(argumentList, "infile:outfile:colname", ["infile=", "outfile=","colname="])
except getopt.GetoptError:
    print('aws-accessreview.py --infile <emails_file> --outfile <report_file> --colname <csv_column_header_name')
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print('aws-accessreview.py --infile <emails_file> --outfile <report> --colname <csv_column_header_name')
        sys.exit()
    elif opt in ("-infile", "--infile"):
        infile = arg
        print('Suspended Email file' + infile)
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
# Log date
today = date.today()
print("Today's date:", today)
# Setup requests header
headers = {'Authorization': 'Bearer {}'.format(auth_token)}
# print(headers)

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
            print('Found user ' + col[emailHeader])
            writer.writerow([col[emailHeader]])
    else:
        print('SCIM user request failed: ' + response.headers['x-amzn-ErrorType'])
    # Don't get rated limited
    time.sleep(.1)

rpt_file.close()
print('Done')