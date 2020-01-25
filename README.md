# Cisco DNA Center Event Subcription
Cisco DNAC supports webhooks for event notifications.
This tool allows CRD on the subscriptions.

## Getting stated
First (optional) step, create a vitualenv. This makes it less likely to clash with other python libraries in future.
Once the virtualenv is created, need to activate it.
```buildoutcfg
python3 -m venv env3
source env3/bin/activate
```

Next clone the code.

```buildoutcfg
git clone https://github.com/CiscoDevNet/DNAC-Subscription.git
```

Then install the  requirements (after upgrading pip). 
Older versions of pip may not install the requirements correctly.
```buildoutcfg
pip install -U pip
pip install -r requirements.txt
```

## Environment variables
The DNAC, username and passowrd of DNAC is specified in environment varaibles.  An example is provided in dnac_vars.
You can edit this file and use the "source" command to put the variables in your shell environment.
```buildoutcfg
source vars_dnac
```


## Listing the Subscriptions
Just running the script with no arguments will print out the current subscriptions.
````buildoutcfg
 ./event.py 
Name:webhook Endpoint:ubunut ConnectorType:REST url:https://10.10.10.10:9001 Count:55 EventIds:NETWORK-DEVICES-2-152,NETWORK-DEVICES-2-153,NETWORK-DEVICES-2-201,NETWORK-DEVICES-2-202,NETWORK-DEVICES-2-204,NETWORK-DEVICES-2-205,NETWORK-DEVICES-3-103,NETWORK-DEVICES-3-104,NETWORK-DEVICES-3-105,NETWORK-DEVICES-3-154,NETWORK-DEVICES-3-155,NETWORK-DEVICES-3-206,NETWORK-DEVICES-3-207,NETWORK-DEVICES-3-208,NETWORK-DEVICES-3-209,NETWORK-DEVICES-3-210,NETWORK-DEVICES-3-211,NETWORK-DEVICES-3-252,NETWORK-DEVICES-3-253,NETWORK-DEVICES-3-254,NETWORK-DEVICES-3-255,NETWORK-DEVICES-3-300,NETWORK-DEVICES-3-304,NETWORK-FABRIC_WIRED-1-308,NETWORK-FABRIC_WIRED-1-310,NETWORK-FABRIC_WIRED-1-311,NETWORK-FABRIC_WIRED-1-312,NETWORK-FABRIC_WIRED-1-315,NETWORK-FABRIC_WIRED-1-317,NETWORK-FABRIC_WIRED-2-309,NETWORK-FABRIC_WIRED-2-313,NETWORK-FABRIC_WIRED-2-314,NETWORK-FABRIC_WIRED-2-316,NETWORK-FABRIC_WIRELESS-1-307,NETWORK-NETWORKS-2-203,NETWORK-NETWORKS-2-256,NETWORK-NETWORKS-2-257,NETWORK-NETWORKS-2-258,NETWORK-NETWORKS-2-259,NETWORK-NETWORKS-2-303,NETWORK-NETWORKS-2-318,NETWORK-NETWORKS-3-100,NETWORK-NETWORKS-3-102,NETWORK-NETWORKS-3-350,NETWORK-NETWORKS-3-351,NETWORK-NETWORKS-3-352,NETWORK-NON-FABRIC_WIRED-1-200,NETWORK-NON-FABRIC_WIRED-1-212,NETWORK-NON-FABRIC_WIRED-1-213,NETWORK-NON-FABRIC_WIRED-1-250,NETWORK-NON-FABRIC_WIRED-1-251,NETWORK-NON-FABRIC_WIRED-1-301,NETWORK-NON-FABRIC_WIRED-2-302,NETWORK-NON-FABRIC_WIRELESS-1-150,NETWORK-NON-FABRIC_WIRELESS-3-156
Name:Temp Endpoint:fred ConnectorType:REST url:https://10.10.10.10:9001 Count:10 EventIds:NETWORK-DEVICES-2-152,NETWORK-DEVICES-2-153,NETWORK-DEVICES-2-201,NETWORK-DEVICES-2-202,NETWORK-DEVICES-2-204,NETWORK-DEVICES-2-205,NETWORK-DEVICES-3-103,NETWORK-DEVICES-3-104,NETWORK-DEVICES-3-105,NETWORK-DEVICES-3-154

````

## Listing the valid events
The --event option shows all of the possible events that can be subscribed to.  
```buildoutcfg
$ ./event.py --event
['NETWORK-DEVICES-3-103', 'NETWORK-DEVICES-3-207', 'NETWORK-NETWORKS-2-318', 'NETWORK-DEVICES-2-201', 'NETWORK-FABRIC_WIRED-1-310', 'NETWORK-FABRIC_WIRED-2-309', 'NETWORK-DEVICES-3-105', 'NETWORK-DEVICES-3-252', 'NETWORK-DEVICES-3-208', 'NETWORK-NON-FABRIC_WIRED-1-250', 'NETWORK-DEVICES-3-254', 'NETWORK-FABRIC_WIRED-1-315', 'NETWORK-NETWORKS-3-351', 'NETWORK-NETWORKS-2-258', 'NETWORK-DEVICES-3-253', 'NETWORK-NON-FABRIC_WIRED-1-251', 'NETWORK-FABRIC_WIRELESS-1-307', 'NETWORK-NON-FABRIC_WIRED-1-200', 'NETWORK-NON-FABRIC_WIRED-2-302', 'NETWORK-DEVICES-3-211', 'NETWORK-DEVICES-3-209', 'NETWORK-DEVICES-3-155', 'NETWORK-FABRIC_WIRED-1-308', 'NETWORK-DEVICES-3-304', 'NETWORK-DEVICES-3-300', 'NETWORK-DEVICES-2-204', 'NETWORK-FABRIC_WIRED-2-316', 'NETWORK-NETWORKS-3-350', 'NETWORK-NETWORKS-2-203', 'NETWORK-DEVICES-2-202', 'NETWORK-DEVICES-3-104', 'NETWORK-NETWORKS-3-100', 'NETWORK-FABRIC_WIRED-1-317', 'NETWORK-NON-FABRIC_WIRELESS-3-156', 'NETWORK-DEVICES-3-210', 'NETWORK-DEVICES-2-152', 'NETWORK-NON-FABRIC_WIRELESS-1-150', 'NETWORK-NETWORKS-2-257', 'NETWORK-NETWORKS-3-352', 'NETWORK-NETWORKS-2-259', 'NETWORK-DEVICES-3-255', 'NETWORK-DEVICES-2-205', 'NETWORK-NETWORKS-3-102', 'NETWORK-DEVICES-3-154', 'NETWORK-NETWORKS-2-256', 'NETWORK-FABRIC_WIRED-2-313', 'NETWORK-FABRIC_WIRED-2-314', 'NETWORK-NETWORKS-2-303', 'NETWORK-DEVICES-3-206', 'NETWORK-FABRIC_WIRED-1-311', 'NETWORK-DEVICES-2-153', 'NETWORK-NON-FABRIC_WIRED-1-301', 'NETWORK-FABRIC_WIRED-1-312', 'NETWORK-NON-FABRIC_WIRED-1-212', 'NETWORK-NON-FABRIC_WIRED-1-213']
55

```
This also takes an optional regular expression.
This example matches all P1/P2 events starting with 3
```buildoutcfg
 ./event.py --event '.*[12]-3[0-9]+'
['NETWORK-NETWORKS-2-318', 'NETWORK-FABRIC_WIRED-1-310', 'NETWORK-FABRIC_WIRED-2-309', 'NETWORK-FABRIC_WIRED-1-315', 'NETWORK-FABRIC_WIRELESS-1-307', 'NETWORK-NON-FABRIC_WIRED-2-302', 'NETWORK-FABRIC_WIRED-1-308', 'NETWORK-FABRIC_WIRED-2-316', 'NETWORK-FABRIC_WIRED-1-317', 'NETWORK-FABRIC_WIRED-2-313', 'NETWORK-FABRIC_WIRED-2-314', 'NETWORK-NETWORKS-2-303', 'NETWORK-FABRIC_WIRED-1-311', 'NETWORK-NON-FABRIC_WIRED-1-301', 'NETWORK-FABRIC_WIRED-1-312']

```

##  Create a new subscription

```buildoutcfg
$ ./event.py --create Adam --events --email fred@adamlab.cisco.com
['NETWORK-DEVICES-3-103', 'NETWORK-DEVICES-3-207', 'NETWORK-NETWORKS-2-318', 'NETWORK-DEVICES-2-201', 'NETWORK-FABRIC_WIRED-1-310', 'NETWORK-FABRIC_WIRED-2-309', 'NETWORK-DEVICES-3-105', 'NETWORK-DEVICES-3-252', 'NETWORK-DEVICES-3-208', 'NETWORK-NON-FABRIC_WIRED-1-250', 'NETWORK-DEVICES-3-254', 'NETWORK-FABRIC_WIRED-1-315', 'NETWORK-NETWORKS-3-351', 'NETWORK-NETWORKS-2-258', 'NETWORK-DEVICES-3-253', 'NETWORK-NON-FABRIC_WIRED-1-251', 'NETWORK-FABRIC_WIRELESS-1-307', 'NETWORK-NON-FABRIC_WIRED-1-200', 'NETWORK-NON-FABRIC_WIRED-2-302', 'NETWORK-DEVICES-3-211', 'NETWORK-DEVICES-3-209', 'NETWORK-DEVICES-3-155', 'NETWORK-FABRIC_WIRED-1-308', 'NETWORK-DEVICES-3-304', 'NETWORK-DEVICES-3-300', 'NETWORK-DEVICES-2-204', 'NETWORK-FABRIC_WIRED-2-316', 'NETWORK-NETWORKS-3-350', 'NETWORK-NETWORKS-2-203', 'NETWORK-DEVICES-2-202', 'NETWORK-DEVICES-3-104', 'NETWORK-NETWORKS-3-100', 'NETWORK-FABRIC_WIRED-1-317', 'NETWORK-NON-FABRIC_WIRELESS-3-156', 'NETWORK-DEVICES-3-210', 'NETWORK-DEVICES-2-152', 'NETWORK-NON-FABRIC_WIRELESS-1-150', 'NETWORK-NETWORKS-2-257', 'NETWORK-NETWORKS-3-352', 'NETWORK-NETWORKS-2-259', 'NETWORK-DEVICES-3-255', 'NETWORK-DEVICES-2-205', 'NETWORK-NETWORKS-3-102', 'NETWORK-DEVICES-3-154', 'NETWORK-NETWORKS-2-256', 'NETWORK-FABRIC_WIRED-2-313', 'NETWORK-FABRIC_WIRED-2-314', 'NETWORK-NETWORKS-2-303', 'NETWORK-DEVICES-3-206', 'NETWORK-FABRIC_WIRED-1-311', 'NETWORK-DEVICES-2-153', 'NETWORK-NON-FABRIC_WIRED-1-301', 'NETWORK-FABRIC_WIRED-1-312', 'NETWORK-NON-FABRIC_WIRED-1-212', 'NETWORK-NON-FABRIC_WIRED-1-213']
{'statusUri': '/dna/intent/api/v1/event/api-status/7b062b42-5987-45ab-9830-6300a1a08ec1'}
{"errorMessage": null, "apiStatus": "SUCCESS", "statusMessage": "Subscription's Adam created "}

```
By default all events are subscribed, but a regexp can be provided to limit the events.

## Delete a subscription
Deletes the subscription named Adam.
````buildoutcfg
 ./event.py --delete Adam 
Deleting subscription Adam id=4b7ac039-74a3-4bbb-a60e-9f791bee89f1
{'statusUri': '/dna/intent/api/v1/event/api-status/8a932475-0489-461a-b982-7908285bfcde'}
{"errorMessage": null, "apiStatus": "SUCCESS", "statusMessage": "Subscription's 4b7ac039-74a3-4bbb-a60e-9f791bee89f1 un-registered "}

````