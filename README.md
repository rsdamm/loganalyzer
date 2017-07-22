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
 
Parse filename parts and set as key based on type of file for all files --done
 
upload each file, and if successful, move to a local 'completed' directory --done

output total size of files and total time it took to upload them all --done

Parse data from file with naming convention:  serverx_Application_name_ts_uniqueid.log
Sample record with fields separated with CRLF
https 
2016-11-27T22:01:26.748203Z 
app/production-gui-alb/5de2d850bc4ae487 
54.252.209.115:44858 
172.25.103.239:80 
0.000 0.066 0.000 
200 200 212 
9834 
"GET https://app.cloudability.com:443/api/2/reporting/compare/reports/7197173/results?auth_token=XsVD9p7opGySzVsCisYh HTTP/1.1" 
"Ruby" 
ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 
arn:aws:elasticloadbalancing:us-east-1:338273444847:targetgroup/production-ec2-webs/ad98e16eb538bde3 
"Root=1-583b57b6-23e3db3136878c9b39771c43"

Extract these fields:
Protocol: https
Timestamp: 2016-11-27T22:01:26.748203Z 
remote client ip w/ port: 54.252.209.115:44858 
3 times: 0.000 0.066 0.000 
3 reponse codes: 200 200 212 
size of request: 9834 
path: after 443 to first question mark /api/2/reporting/compare/reports/7197173/results

## Desired Information
Average load time per result as a histogram hour-by-hour


Git work