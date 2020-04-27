#!/usr/bin/python3

# construct post_install_inventory.yml from *ocpinventory.json
# provided by the scale lab
# assumes only one machine type per cloud
# prints to stdout, you have to redirect to file
# example:
# python3 mk_post_install_inventory_yml.py \
#    http://quads.rdu2.scalelab.redhat.com/cloud/cloud08_ocpinventory.json

import json, os, sys, urllib3
from sys import argv

def usage(msg):
    print('ERROR: ' + str(msg))
    print('usage: mk_post_install_inventory_yml.py URL')
    sys.exit(1)

# parse command line parameters

if len(argv) < 2:
    usage('too few command line parameters')
cloud_metadata_url = argv[1]

# read metadata about this scale lab cloud

http = urllib3.PoolManager()
response = http.request('GET', cloud_metadata_url)
cloud_dict =  json.loads(response.data)
cloud_nodes = cloud_dict['nodes']
deployer_dict = cloud_nodes[0]
masters_dict = cloud_nodes[1:4]
workers_dict = []
if len(cloud_nodes) > 4:
  workers_dict = cloud_nodes[4:]

# print out the inventory file
# strip off the "mgmt-" prefix from the hostnames in the json 

print('---')
print('# generated by inventory_with_macs.yml from *ocpinventory.json')
print('# ansible inventory file for after openshift install\n#   using URL %s' % 
    cloud_metadata_url)
print('')

print('deployer:')
print('  hosts:')
print('    %s:' % deployer_dict['pm_addr'][5:])
print('')

print('masters:')
print('  hosts:')
for k, m in enumerate(masters_dict):
 print('    master-%d:' % k)
print('')

if len(workers_dict) > 0:
 print('workers:')
 print('  hosts:')
for j, w in enumerate(workers_dict):
 print('    worker-%02d:' % j)
print('')

print('all_openshift:')
print('  children:')
print('    masters:')
print('    workers:')

