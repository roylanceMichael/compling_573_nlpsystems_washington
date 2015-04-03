#
#  Condor job file for ling573 
#  Author: Thomas Marsh
#  Date: 4/2/2015
#
Executable = ../ling573.sh
Universe   = vanilla
getenv     = true
transfer_executable = false
request_memory = 2*1024

output     = ling573.condor.output
error      = ling573.condor.stderror
Log        = ling573.condor.log
arguments  = "arg1 arg2 arg3"
Queue