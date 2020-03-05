#!/bin/bash
# execute a command in parallel on a set of host specified in param 1
# you must quote the command if it's more than a single word
# parameter 1: file containing list of hostnames/IPs, 1 host per record
# parameter 2: the command to execute
source ~/.bashrc

if [ -z "$QUADS_TICKET" ] ; then
  echo "must specify reservation ticket number in QUADS_TICKET env. var."
  exit 1
fi

export password=$QUADS_TICKET
echo "reading host list from $1"
echo

logdir=/tmp/par-for-all.$$
echo "log directory is $logdir"
hostlist_file=$1
OK=0

#echo "starting in parallel on : "
rm -rf $logdir && mkdir -p $logdir

export hostlist="`cat $1`"
shift

for n in $hostlist ; do 
  #echo -n " $n" 
  cmd="/usr/bin/python3 ./badfish/badfish.py -u quads -p $password -i ./badfish/config/idrac_interfaces.yml -H "
  echo
  echo "for host $n"
  echo "$cmd $n $*"
  echo "log file: $logdir/$n.log"
  #eval "$cmd $n $*"
  
  eval "$cmd $n $* > $logdir/$n.log 2>&1 &"
  pids="$pids $!"
  mydir=`dirname $0`
  # throttle the launching of parallel threads
#  ( echo 'import time' ; echo 'time.sleep(0.1)' ) | python
  sleep 0.1
done

echo "\nWaiting..."
j=0
host_array=( `cat $hostlist_file` )
#host_array=$hostlist

for p in $pids ; do 
  h=${host_array[$j]}
  wait $p
  s=$?
  chars=`wc -c < $logdir/$h.log`
  if [ $chars -ge 1 -o $s != $OK ] ; then
    echo
    echo "--- $h ---"
    if [ $s != $OK ] ; then
      echo "pid $p on host $h returns $s"
    fi
    cat $logdir/$h.log
  fi
  retcodes="$retcodes $s"
  (( j = $j + 1 ))
done

for s in $retcodes ; do
  if [ $s != $OK ] ; then exit $s ; fi
done
exit $OK
