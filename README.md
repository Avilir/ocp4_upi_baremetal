This is an ansible playbook for implementing Dustin Black's method for doing OpenShift 4 UPI installation 
on baremetal machines in the Red Hat (IBM) Perf & Scale Alias lab.  To run it:

ansible-playbook -i your-inventory.yml ocp4_upi_baremetal.yml

your inventory file should look something like this example:
```
[deployer]
e26-h01-740xd.alias.bos.scalelab.redhat.com

[masters]
e26-h03-740xd.alias.bos.scalelab.redhat.com
e26-h05-740xd.alias.bos.scalelab.redhat.com
e26-h07-740xd.alias.bos.scalelab.redhat.com

[workers]
e26-h09-740xd.alias.bos.scalelab.redhat.com
e26-h11-740xd.alias.bos.scalelab.redhat.com
```
