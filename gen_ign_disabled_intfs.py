#!/usr/bin/python3
# gen_ign_disabled_intfs.py
# script to auto generate disabled interfaces
# in form that ignition can consume them

import yaml
from sys import argv, exit
import os

def myabort(msg):
  print('ERROR: ' + msg)
  print('usage: %s your-lab-metadata.yml ignition-dir lab-name' % argv[0])
  exit(1)

if len(argv) < 3:
  usage('not enough CLI parameters')

metadata_fn = argv[1]
ignition_dir = argv[2]
lab_name = argv[3]

with open(metadata_fn, 'r') as metaf:
  # FIXME: unsafe
  d = yaml.load(metaf, Loader=yaml.SafeLoader)

metadata = d['lab_metadata']
lab_machine_types = None
for lab in metadata:
  if lab['name'] == lab_name:
    lab_machine_types = lab['machine_types']
if not lab_machine_types:
  usage('lab name not found')

for minfo in lab_machine_types:
  mtype = minfo['machine_type']
  disabled_intfs = minfo['disabled_intfs']
  relpath = ignition_dir + '/' + str(mtype) + '/' + 'etc/sysconfig/network-scripts'
  os.makedirs(relpath, exist_ok=True)
  for i in disabled_intfs:
     with open(os.path.join(relpath, 'ifcfg-%s' % i), 'w') as iff:
       iff.write('DEVICE=%s\nONBOOT=no\nBOOTPROTO=none\n' % i)



