import boto3
s3 = boto3.resource('s3')

#upload a file
object_key = 'docs2013-09-12-23-22-02.txt'
data = open('Z:/Programming/log_input_data/docs2013-09-12-23-22-02-F23F3B082CFF53EF.txt', 'r')
s3.Bucket('loganalyzer-bucket').put_object(Key=object_key, Body=data)