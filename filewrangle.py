#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
 
import sys
import re
import os
import shutil
import commands
import boto3
import time
from datetime import datetime
import time
   
def process_files(from_dir, post_dir, bucket_name):  
  i=0
  s3 = boto3.resource('s3')
  bucket = s3.Bucket(bucket_name)
  exists = True
  total_file_size = 0
  total_time_to_upload = 0
  try:
      s3.meta.client.head_bucket(Bucket=bucket_name)
  except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False 
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  if exists:
     print ("Start time: %s" % current_time)
     print ("Bucket %s exists " % bucket_name)
     print ("Uploading files from directory: %s" % from_dir)
     print ("Post processing directory : %s " % post_dir)
  else: 
    print ("Bucket %s does not exist -exiting" % bucket_name)
    return
    
  #for filename in filenames:
  filenames = os.listdir(from_dir)
  
  start_time = datetime.now()  
  for filename in filenames:  
    from_dir_filename = os.path.join(from_dir, filename)
    post_dir_filename = os.path.join(post_dir, filename)
    object_key = get_key(filename)  
    
    if object_key: 
       i+=1
       total_file_size = total_file_size + os.path.getsize(from_dir_filename)/1024
       bucket.put_object(Key=object_key, Body=from_dir_filename) 
       print ("%s Uploaded: %s with key %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), from_dir_filename, object_key))
       #copy_to(from_dir_filename, post_dir, post_dir_filename)
       move_to(from_dir_filename, post_dir, post_dir_filename) 
       
  end_time = datetime.now()
  
  #total_time_to_upload = relativedelta(end_time, start_time)
  total_time_to_upload = end_time - start_time
    
  print ("%s ***Processing complete***  File count: %d Size: %d kb Total time to upload:   %s seconds" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i, total_file_size, total_time_to_upload.seconds))
  return 
  
def get_key(filename):
  object_key = ''  
  keyparts = filename.split("_")  
  if len(keyparts) > 1:
     if keyparts[0] == "ServiceName":
        object_key = get_service_format_key(keyparts)
     elif keyparts[1] == "ApplicationName":
          object_key = get_app_format_key(keyparts) 
  #skip anything else     
  return object_key
  
def get_service_format_key(keyparts):
# return type server date and datetime
  return keyparts[0] + "_" + keyparts[2] + "_" + keyparts[1] + ".log.gz"
  
def get_app_format_key(keyparts):
  # return type server date and datetime
  return keyparts[1] + "_" + keyparts[0] + "_" + keyparts[2] + ".log.gz"
  
def get_doc_format_key(keyparts):
  # return type server date and datetime
  return  keyparts[0] 
  
def copy_to(from_file_dir, post_dir, post_dir_file): 
    if not os.path.exists(post_dir):   
        os.mkdir(post_dir)   

    shutil.copy(from_file_dir, post_dir_file)
    return

def move_to(from_file_dir, post_dir, post_dir_file): 
    if not os.path.exists(post_dir):   
        os.mkdir(post_dir)   

    shutil.move(from_file_dir, post_dir_file)
    return 
    
def main():
  print ('--------------------------------------------------------------------------')
  result = []
  # This basic command line argument parsing code is provided. 

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print ("usage: --[fromdir] dir --[postdir] dir --[bucketname] bucketname")
    #C:\Users\REnee\git\loganalyzer>py filewrangle.py --fromdir Z:\Programming\log_input_data --postdir Z:\Programming\done_data  --bucketname loganalyzer-bucket
    sys.exit(1)

  if len(args) <> 6:
    print ("error: provide from and post processing directories")
    sys.exit(1)

  # dir is set from command line
  # or left as the empty string. 
  fromdir = ''
  if args[0] == '--fromdir':
    fromdir = args[1]
    del args[0:2]
        
  postdir = ''
  if args[0] == '--postdir':
    postdir = args[1]
    del args[0:2]
          
  bucketname = ''
  if args[0] == '--bucketname':
    bucketname = args[1]
    del args[0:2]
        
  if fromdir and postdir and bucketname:
    print ("Source file directory: %s " % fromdir)   
    print ("Post processing directory: %s" % postdir)
    print ("S3 bucketname: %s" % bucketname)
    print ("  ")
    print ("  " )
    process_files(fromdir, postdir, bucketname)
  else:
    print ('\n'.join(result))
 
if __name__ == "__main__":
  main()
