#!/usr/bin/env python
from __future__ import print_function
import time
import json
import requests
import logging
import re
# turn off warninggs
requests.packages.urllib3.disable_warnings()
import re
from datetime import datetime

from dnac_config import DNA_CENTER_BASE_URL, DNA_CENTER_USERNAME, DNA_CENTER_PASSWORD
from argparse import ArgumentParser
from dnacentersdk import api

logger = logging.getLogger()

class Event():
    def __init__(self, dnac):
        self.dnac = dnac
        self.response = self.get_subscriptions(dnac)
        self.events = self.get_events(dnac)
        self.eventIds = self.get_event_ids()

    @staticmethod
    def get_events(dnac):
        count = dnac.custom_caller.call_api(method="GET",
                                               resource_path="dna/intent/api/v1/events/count?tags=ASSURANCE")
        response = dnac.custom_caller.call_api(method="GET",
                                               resource_path="dna/intent/api/v1/events?tags=ASSURANCE&limit={}".format(count.response))
        #print(json.dumps(response))
        return response

    def get_event_ids(self):
        return [event.eventId for event in self.events]

    @staticmethod
    def get_subscriptions(dnac):
        response = dnac.custom_caller.call_api(method="GET",
                                                          resource_path="dna/intent/api/v1/event/subscription")
        #print(json.dumps(response))
        return response

    def lookup(self, subs):
        return  [e.subscriptionId for e in self.response if e.name == subs]

    def delete_event(self, subid):
        url = "dna/intent/api/v1/event/subscription?subscriptions={}".format(subid)
        response = self.dnac.custom_caller.call_api(method="DELETE", resource_path=url)
        print(response)
        self.show_response(response)

    def create_event(self, payload):
        url = "dna/intent/api/v1/event/subscription"
        response = events.dnac.custom_caller.call_api(method="POST", resource_path=url, data=json.dumps(payload))
        print(response)
        self.show_response(response)

    def show_response(self, response):
        url = response.statusUri
        while True:
            task = dnac.custom_caller.call_api("GET", url)
            if task.apiStatus != "IN_PROGRESS":
                #print('retry')
                break
        print(json.dumps(task))

    def match_events(self, regexp):
        #.*-[3]-[0-9]+
        return [eventid for eventid in self.eventIds if re.match(regexp, eventid)]

def del_sub(events, subs):
    # what is format of subs?
    # only does single subscription at present

    subid = events.lookup(subs)

    if len(subid) <1:
        print("Could not find subscription named {} to delete".format(subs))
        return
    print('Deleting subscription {} id={}'.format(subs, subid[0]))
    events.delete_event(subid[0])

def create_sub(**args):
    '''
    creates a new subscription.  can be either REST or EMAIL based
    :param args:
    :return:
    '''
    events = args.pop('events')
    name = args.pop('name')
    regexp = args.pop('regexp')
    url = args.pop('url')
    email = args.pop('email')
    eventids = events.match_events(regexp)
    print(eventids)
    sub_email =  {
        "subscriptionDetails": {
          "connectorType": "EMAIL",
          "name": "Email",
          "description": "created by API",
          "fromEmailAddress": "maglev@adamlab.cisco.com",
          "toEmailAddresses": [
            email
          ],
          "subject": "DNAC Event"
        }
      }

    sub_rest= {
        "subscriptionDetails":{
            "connectorType": "REST",
          "name": "fred",
          "description": "created by API",
          "url": url,
          "method": "POST",
          "trustCert": False,
        }

    }
    if email is not None:
        sub = sub_email
    else:
        sub = sub_rest
    payload =  [{
    "name": name,
    "description": "",
    "subscriptionEndpoints": [
        sub
    ],
    "filter": {
      "eventIds": eventids,
      "others": []
    },
    "isPrivate": False,
    }]

    events.create_event(payload=payload)

def parse_sub_detail(detail):

    result = 'ConnectorType:{}'.format(detail.connectorType)
    if  detail.connectorType == "REST":
        return  result + ' url:{}'.format(detail.url)
    else:
        return result + ' Email:{}'.format(','.join(detail.toEmailAddresses))

def show_subs(events):
    '''
    displays subscriptions and the events
    :param events:
    :return:
    '''
    logging.debug(json.dumps(events.response, indent=2))
    subscriptions = ["Name:{} Endpoint:{} {} Count:{} EventIds:{}".format(s.name,
                            s.subscriptionEndpoints[0].subscriptionDetails.name,
                            parse_sub_detail(s.subscriptionEndpoints[0].subscriptionDetails),
                            len(s.filter.eventIds),
                                 ','.join(s.filter.eventIds)) for s in events.response]
    print("\n".join(subscriptions))

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    add_group = parser.add_mutually_exclusive_group()
    add_group.add_argument('--url',type=str, required=False, help='url for REST enpoint')
    add_group.add_argument('--emailAddress', type=str, required=False, help='email address for EMAIL notification')
    parser.add_argument( '-d', "--delete", type=str, required=False, help='delete')
    parser.add_argument('-c', "--create", type=str, required=False, help='create a subscription with this name')

    parser.add_argument('-e', "--events", type=str, required=False, nargs='?',const='.*',
                        help='event filter, default is ".*", e.g. ".*-[12]-1[0-9]+"')
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()


    if args.v:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        # set logger
    logger.debug("Logging enabled")
    logging.debug("Vars:{}".format(vars(args)))

    dnac = api.DNACenterAPI(base_url=DNA_CENTER_BASE_URL,
                            username=DNA_CENTER_USERNAME, password=DNA_CENTER_PASSWORD, verify=False)
    events = Event(dnac)
    if args.delete:
        del_sub(events, args.delete)
    elif args.create:
        create_sub(events=events, name=args.create, regexp=args.events, email=args.emailAddress,url=args.url)
    elif args.events:
        print(events.match_events(args.events))
        print (len(events.match_events(args.events)))
    else:
        show_subs(events)
