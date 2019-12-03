#!/usr/local/bin python3
import requests
import json
import re
import getpass
import time
from datetime import datetime, timedelta
from urllib3.exceptions import InsecureRequestWarning

#Create a file for logging activity 
timestr = time.strftime("%Y%m%d")
f= open("bulk-deleted-apps-" +timestr+ ".txt","w+")

#Get Login Information from command line
try:
        iq_user = getpass.getuser()
except Exception as error:
        print ('ERROR', error)
else:
        print ('User is: ', iq_user)

try:
        iq_password = getpass.getpass()
except Exception as error:
        print ('ERROR', error)
else:
        print ('Password is: correct ')

startTime = str(datetime.now())

#Adjust this URL to test or prod
iq_server_url = 'https://URL-to-your-server'

#Get a list of applications
#Check https://help.sonatype.com/iqserver/automating/rest-apis/application-rest-apis---v2 for more details on
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)   #disables warnings when testing on non aliased servers
request_response = requests.get(iq_server_url + '/api/v2/applications',auth=(iq_user, iq_password), verify=False)
response_json = request_response.json()

#print (response_json)  #<--- ucomment for troubleshooting
iq_applications = response_json['applications']

#Loop through applications to get a list of reports
#Each application can have a report at each stage, so 
#ensure NONE are less than X days old - example below is 30 days
for iq_application in iq_applications:
        iq_app_id = iq_application["id"]
        iq_app_name = iq_application["name"]

        #get application reports
        reports_response = requests.get(iq_server_url +'/api/v2/reports/applications/' + iq_app_id, auth=(iq_user, iq_password), verify=False)
        iq_reports = reports_response.json()
        
        # Loop through the reports and get the date and test the age
        reportCtr = 0

        for iq_report in iq_reports:
                evaluationDate = iq_report['evaluationDate']
                evaluationDate, evaluateTime = evaluationDate.split("T",1)
                reportDate = datetime.strptime(evaluationDate, '%Y-%m-%d')
                delta = datetime.now() - timedelta(days=30) 

                #Test if report date is newer than 30 days - if so increment counter
                if(reportDate > delta):  
                     reportCtr = reportCtr + 1

        #no reports newer than 30 days - ok delete 
        if reportCtr < 1:
                        print ("deleting " + iq_app_name + " with app id " + iq_app_id)
                        f.write("moved " + iq_app_name + "\n")
                        delete_reponse = requests.delete(iq_server_url + '/api/v2/applications/' + iq_app_id,auth=(iq_user, iq_password), verify=False)        
 
        #reset report counter
        reportCtr = 0               

#close the file
f.close()
endTime = (str(datetime.now()))
print ("started " + startTime + " end time " +  endTime)
