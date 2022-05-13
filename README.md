# aws-ssoreporting
Thank you very little AWS API team responsible for SSO. 
I needed a down and dirty script to report AWS SSO users and groups. Why AWS makes this so hard is just beyond reason. 
To run this you need:
1. A file with every email address in your directory. The CSV needs a header row. Put the email address column name in --colname paramter.
2. AWS SSO SCIM URL stored in env variable URL. Found in the AWS SSO console. 
3. AWS SSO SCIM auth token stored in env variable SCIMTOKEN. Found in the AWS SSO console. 

python aws-ssoreporting.py --infile=<emails_file> --outfile=<report_file> --colname=<email_addr_column_name>

 Output rpt file is one row for every group a user is a member of
 email,firstname,lastname,groupname
 
