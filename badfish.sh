#!/bin/bash
if [ -z "$QUADS_TICKET" ] ; then
  echo "must specify reservation ticket number in QUADS_TICKET env. var."
  exit 1
fi
export password=$QUADS_TICKET
echo "reading host list from $1"
echo
export hostlist="`cat $1`"
shift
for m in $hostlist ; do
  cmd="python3 badfish/badfish.py -u quads -p $password -i badfish/config/idrac_interfaces.yml -H "
  # command line parameters are passed through to badfish
  echo
  echo "for host $m"
  echo $cmd $m $*
  eval "$cmd $m $*"
done
