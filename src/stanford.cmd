#
#  Condor job file for ling573 
#  Author: Brandon Gahler
#  Date: 5/16/2015
#
Executable = /opt/python-2.7/bin/python2.7
arguments  = "cacheCompressStanford.py"
Universe   = vanilla
getenv     = true
transfer_executable = false
request_memory = 2*1024

output     = stanford.output
error      = stanford.stderror
Log        = stanford.log
Queue
