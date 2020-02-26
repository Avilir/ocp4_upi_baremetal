This repo contains 2 ansible playbooks for implementing Dustin Black's method for doing OpenShift 4 UPI installation 
on baremetal machines in the Red Hat (IBM) Perf & Scale Alias lab.   Dustin's document is [at this link](https://docs.google.com/document/d/1hl2qVWyRjqhKT3ZR5Q2xn9Ip1DLShanxQcnp11Zf1tw/edit?ts=5e5462d2#heading=h.f51z993ev25
).


The first step happens when you get your lab reservation.  At this time, there is usually a vanilla Linux distro installed on all the machines that you can use to discover information about your cluster using ansible fact-gathering.  You run the discover_macs.yml playbook one time, to generate an inventory file with mac addresses defined for all machines.   For example, construct an input inventory file like this one, call it basic_inv.yml:

```
[deployer]
e26-h01-740xd.alias.bos.scalelab.redhat.com

[masters]
e26-h03-740xd.alias.bos.scalelab.redhat.com
e26-h05-740xd.alias.bos.scalelab.redhat.com
e26-h07-740xd.alias.bos.scalelab.redhat.com

[workers]
e26-h09-740xd.alias.bos.scalelab.redhat.com
```

Next, ensure that you have password-less ssh access to all the machines in this inventory, using ssh-copy-id if this has not been set up already.  You may need to clear out ~/.ssh/known_hosts entries for previous incarnations of these hosts.

Now run the first playbook to get an output inventory file with mac addresses filled in.

```
ansible-playbook -vv --private-key ~/.ssh/id_rsa_perf -i /tmp/w.yml discover_macs.yaml
```

This should output a file named **inventory_with_macs.yml** by default - it will look the same as your previous inventory but with per-host deploy_mac variable added to each record.   From now on, you use this as your inventory file, not the preceding one.

Then define your cluster parameters by doing:

```
cd group_vars
cp all.yml.sample all.yml
<edit all.yml>
cd ..
```

At present the playbook relies on subscription manager to get RHEL8 repos that you need.   You need to do just one command on the deployer:

```
subscription-manager register
Username:your-account@redhat.com
Password:your-password
```

Now you set up your deployment with:

```
ansible-playbook -i inventory_with_macs.yml ocp4_upi_baremetal.yml
```

This playbook can be used whenever a re-install of the deployer host is needed, regardless of what state the masters and workers are in.

Dustin's document describes what the playbook should be doing.  This will take a long while, and may involve the reboot of the deployer host and download of RHCOS and openshift.   When it finishes, you will have a deployer host that is set up to install masters and workers.   We do not actually install the masters and workers in this playbook.   

To trigger the start of this process, use the installed **badfish.sh**.  It applies commands to a list of hosts in a file.  At present, it only supports the Dell 740xds in the Alias lab, but should work with most Dell machines.    See Dustin's notes about supermicro alternative procedures.   **badfish.sh** depends on the **QUADS_TICKET** environment variable defined in **~/.bashrc**  - you can source it or logout and login again.

```
badfish.sh masters.list -t director
badfish.sh masters.list --pxe
badfish.sh masters.list --check-boot
badfish.sh masters.list --power-cycle
```

If all goes well, then the bootstrap VM should install CoreOS and ignition files on all of these machines and they should reboot and join the OpenShift cluster.  Once that has happened, you can then install the workers with the same procedure, substituting workers.list for masters.list.

When you are done with the cluster, use

```
for typ in masters workers ; do badfish.sh $typ.list -t foreman ; done
```

to revert the boot order to the original state that the labs expect.
