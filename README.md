# loganalyzer
## Description

##Task List

Create S3 bucket using AWS console (website)  --done

Use Python or Java to upload objects (files) to bucket --done

Review GIT and put python code in github --done

### Bulk file upload
There are two different formats in the log_input_data directory.
    ExampleFilename: server2_ApplicationName_20161127T2205Z_46p3o742.log.gz
    FilenameParts:  servername  appname    timestamp(zulu)  randomId

    ExampleFileName2: ServiceName_20160910T2340Z_server6_105vwltg.log.gz
    FilenameParts:      appname   timestamp(zulu) servername   randomId
 
Parse filename parts and set as key based on type of file for all files
upload each file, and if successful, move to a local 'completed' directory
output size of file and time it took to upload 

give set of files to hadoop

## Desired Information
Average load time per result
