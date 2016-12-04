#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
 
import sys
import re
import os
import shutil
import commands
 
def split_filenames(from_dir, post_dir):
  dirlist = []
  
  fmt = ""
  #for filename in filenames:
  filenames = os.listdir(from_dir)
  
  for logfile in filenames:
  #  print logfile
  # dirlist.append(os.path.abspath(os.path.join(fromdir, filename)))
    print logfile.split(str="_") 
  #print os.path.splitext(logfile) 
  #print '\n'.join(result)
  return dirlist
  
def copy_to(filename, postdirname): 
    if not os.path.exists(postdirname):   
        os.mkdir(postdirname)  

    shutil.copy(path, os.path.join(to_dir, filename))
    return
    
def main():
  print '--------------------------------------------------------------------------'
  result = []
  # This basic command line argument parsing code is provided. 

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: --[fromdir] dir --[postdir] dir";
    sys.exit(1)

  if len(args) <> 4:
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
          
  if fromdir and postdir:
    print "Source file directory: " + fromdir   
    print "Post processing directory: " + postdir 
    result.extend(split_filenames(fromdir, postdir)) 
  else:
    print '\n'.join(result)
 
if __name__ == "__main__":
  main()
