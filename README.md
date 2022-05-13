# aws-ssoreporting
Thank you very little AWS API team working SSO. 
I need a down and dirty script to report AWS SSO users and groups. Why AWS makes this so hard is just beyond reason. 
To run this you need:
1. A file with every email address in your directory, one per row. 
2. A SCIM URL stored in env variable URL. Found in the AWS SSO console. 
3. A SCIM auth token stored in env variable SCIMTOKEN. Found in the AWS SSO console. 

aws-ssoreporting.py --infile <emails_file> --outfile <report>

 Output file is one row for every group a user is a member of
 email,firstname,lastname,groupname
