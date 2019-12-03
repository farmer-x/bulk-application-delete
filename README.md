# bulk-application-delete
A python script that uses the Nexus IQ Server API to automate deleting multiple applications which have not created a new report w/i a defined timeframe.


## Pre-requisites
- Python 3.7 installed
- Appropriate level access on Nexus IQ Server to delete applications  

## How to use
Copy to a working directory where you have permission to write.

- To run: `$ python3.7 bulk-app-delete.py`
- Enter your login and password at the prompt
- Run time depends on the number of applications and the speed of your network connection

### Notes:
Running this script will create a log file named using the date of when the script was run and includes the names of applications that were deleted. Example: `bulk-deleted-apps-20191202.tx` 

To get a quick count of how many applications were deleted (Linux/Mac) - `$ wc -l bulk-deleted-apps-20191202.tx`

By default, as each application is deleted it will be printed to the terminal screen.

Line 36: Optional - handles requests to hosts with certificate issues.

