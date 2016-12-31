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
    
def process_files(from_dir, post_dir, bucket_name):  
  s3 = boto3.resource('s3')
  bucket = s3.Bucket(bucket_name)
  exists = True
  try:
      s3.meta.client.head_bucket(Bucket=bucket_name)
  except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False 
  if exists:
     print "Bucket " + bucket_name + " exists" 
  else: 
    print "Bucket " + bucket_name + " does not exist -exiting"
    return
    
  #for filename in filenames:
  filenames = os.listdir(from_dir)
  
  for filename in filenames:  
    file_dir = os.path.join(from_dir, filename)
    object_key = get_key(filename)  
    print ("Uploading: " + filename)
    if object_key: 
       bucket.put_object(Key=object_key, Body=file_dir) 
       copy_to(file_dir, post_dir, filename)
       #move_to(file_dir, post_dir, filename)
  #print '\n'.join(result)
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
  
def copy_to(file_dir, post_dir, filename): 
    if not os.path.exists(post_dir):   
        os.mkdir(post_dir)   

    shutil.copy(file_dir, os.path.join(post_dir, filename))
    return

def move_to(file_dir, post_dir, filename): 
    if not os.path.exists(post_dir):   
        os.mkdir(post_dir)   

    shutil.copy(file_dir, os.path.join(post_dir, filename))
    return 
    
def main():
  print '--------------------------------------------------------------------------'
  result = []
  # This basic command line argument parsing code is provided. 

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: --[fromdir] dir --[postdir] dir --[bucketname] bucketname";
    sys.exit(1)

  if len(args) <> 6:
    print "error: provide from and post processing directories"
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
    print "Source file directory: " + fromdir   
    print "Post processing directory: " + postdir 
    print "S3 bucketname: " + bucketname
    print "  " 
    print "  " 
    process_files(fromdir, postdir, bucketname)
  else:
    print '\n'.join(result)
 
if __name__ == "__main__":
  main()
