#!/usr/bin/python
import adif_io
import xml.etree.ElementTree as ET #rip unstrusted
import sys
import argparse

#TODO: include band based on "frequency" attrib (first two digits?)
#TODO: parse wsjtx_adi to see if i've worked them before
# check the band
#TODO: download files from pskreporter
#TODO: add last heard/seen?
#TODO: read from "who I heard via _ALL.txt" instead of pskreporter? grep it for the call + time minus my call if it comes after it.

wsjtxfile = "wsjtx_log.adi"
receivertag = "activeReceiver" #stations that are actively listening
receptionreporttag = "receptionReport" #stations that heard US
activecallsigntag = "activeCallsign" #???
mycallsign = "ZL4KYH" #changeme
mode = "FT8"
heardmecallsigns = [] #callsigns that are hearing me
iheardcallsigns = [] #callsigns i've heard from pskreporter
txactivereceivers = [] #callsigns that are activerecievers.
rxactivereceivers = [] #callsigns that are activerecievers.
alllogfile = "202402_ALL.TXT"
#https://retrieve.pskreporter.info/query?senderCallsign=CALLSIGN&appcontact=emailaddress" for who heard us.
#  <receptionReport receiverCallsign="WA6OUR-K" receiverLocator="CN87xo" senderCallsign="ZL4KYH" senderLocator="RE78js" frequency="24917631" flowStartSeconds="1707517560" mode="FT8" isSender="1" receiverDXCC="United States" receiverDXCCCode="K" sNR="-17" />

#https://retrieve.pskreporter.info/query?receiverCallsign=CALLSIGN&appcontact=emailaddress for who we heard 
#  <receptionReport receiverCallsign="ZL4KYH" receiverLocator="RE78js" senderCallsign="N7BC" senderLocator="CN87ql20" frequency="24915356" flowStartSeconds="1707517048" mode="FT8" isReceiver="1" senderRegion="Washington" senderDXCC="United States" senderDXCCCode="K" senderDXCCLocator="EM47" senderLotwUpload="2024-02-04" senderEqslAuthGuar="A" sNR="-6" />

#qsos, header = adif_io.read_from_file("test1.adi")
#print("QSOS: {}".format(qsos, header))
def checkactivereceiver(callsign):
    ''' takes a callsign and returns true if it's an activereceiver'''
    for child in txroot:
        if child.tag == "activeReceiver":
            if args.verbose:
                print(child.tag, child.attrib)
                print("this is an activeReceiver ", child.attrib.get('callsign'))
            txactivereceivers.append(child.attrib.get('callsign'))
    for child in rxroot:
        if child.tag == "activeReceiver":
            if args.verbose:
                print(child.tag, child.attrib)
                print("this is an activeReceiver ", child.attrib.get('callsign'))
            rxactivereceivers.append(child.attrib.get('callsign'))
    if callsign in txactivereceivers:
        return True
    elif callsign in rxactivereceivers:
        return True
    else:
        return False

def returnband(frequency):
    #frequency="14074686" etc
    ''' check the first two digits and return a band, ie 14 for 20M'''
    if frequency[0:2] == "50":
        return "6M"
    elif frequency[0:2] == "28":
        return "10M"
    elif frequency[0:2] == "24":
        return "12M"
    elif frequency[0:2] == "21":
        return "15M"
    elif frequency[0:2] == "181":
        return "17M"
    elif frequency[0:2] == "14":
        return "20M"
    elif frequency[0:2] == "10":
        return "30M"
    elif frequency[0:2] == "70":
        return "40M"
    elif frequency[0:2] == "53":
        return "60M"
    elif frequency[0:2] == "35":
        return "80M"
    elif frequency[0:2] == "184": #assumption made here, see also 17M
        return "12M"
    else:
        #wah
        return "UNKNOWN"
    
def checkwsjtxalllogsingle(callsign): 
    #durp, this isn't xml, assumes its for the right band
    alllogfilehandle = open(alllogfile, 'r')
    allloglines = alllogfilehandle.readlines()
    if args.verbose:
            print("in checkwsjtxalllogsingle")

    for line in allloglines:
        if args.verbose:
            print(line)
        if "CQ " + callsign in line:
            return True
        elif callsign + " RRR" in line:
            return True
        elif callsign + " RR73" in line:
            return True
        elif callsign + " 73" in line:
            return True
        elif callsign in line:
            return True
    return False

def checkwsjtxalllogmultiple(callsigns): 
    #durp, this isn't xml, assumes its for the right band
    alllogfilehandle = open(alllogfile, 'r')
    allloglines = alllogfilehandle.readlines()
    for callsign in callsigns:
        if callsign in allloglines:
            if "CQ " + callsign in allloglines:
                return True
            elif callsign + " RRR" in allloglines:
                return True
            elif callsign + " RR73" in allloglines:
                return True
            elif callsign + " 73" in allloglines:
                return True
        else:
            return False
        
parser = argparse.ArgumentParser()
callsigngroup = parser.add_mutually_exclusive_group()
callsigngroup.add_argument('-c', '--callsign', help="Callsign to search for for bidirectional")
callsigngroup.add_argument('-ctx', '--callsigntx', help="Callsign to search for can we hear them")
callsigngroup.add_argument('-crx', '--callsignrx', help="Callsign to search for can they hear us")
parser.add_argument('-cwa', dest='checkwsjtxall', action='store_true', help="Check wsjtx ALL log") #don't do rx download if we use this.
parser.add_argument('-v', dest='verbose', action='store_true', help="Verbose mode")
args = parser.parse_args()


#need to skip this if we are using the wsjtx log
txtree = ET.parse('test3rx.adi')
txroot = txtree.getroot()
for child in txroot:
    if child.tag == "receptionReport":
        if args.verbose:
            print(child.tag, child.attrib)
            print("I heard ", child.attrib.get('senderCallsign'))
        iheardcallsigns.append(child.attrib.get('senderCallsign'))

rxtree = ET.parse('test2.adi')
rxroot = rxtree.getroot()

for child in rxroot:
    if child.tag == "receptionReport":
        if args.verbose:
            print(child.tag, child.attrib)
            print("heard me ", child.attrib.get('receiverCallsign'))
        heardmecallsigns.append(child.attrib.get('receiverCallsign'))




workableset = set(heardmecallsigns).intersection(iheardcallsigns)        
workablelist = sorted(workableset)
print(workablelist)


    

if args.callsign: #this is in both directions
    if args.callsign in workablelist:
        print(args.callsign + " is workable, activereceiver:", checkactivereceiver(args.callsign))
        if args.checkwsjtxall:
            print("in wsjtx all log?:", checkwsjtxalllogsingle(args.callsign))
    else:
        print(args.callsign + " is not workable, activereceiver:", checkactivereceiver(args.callsign))
        if args.checkwsjtxall:
            print("in wsjtx all log?:", checkwsjtxalllogsingle(args.callsign))
elif args.callsigntx: #this is if we can hear them
    if args.callsigntx in iheardcallsigns:
        print(args.callsigntx + " is hearable, activereceiver:", checkactivereceiver(args.callsigntx))
        if args.checkwsjtxall:
            print("in wsjtx all log?:", checkwsjtxalllogsingle(args.callsign))
    else:
        print(args.callsigntx + " is not hearable, activereceiver:", checkactivereceiver(args.callsigntx) )
        if args.checkwsjtxall:
            print("in wsjtx all log?:", checkwsjtxalllogsingle(args.callsign))
elif args.callsignrx: #this is if they can hear us
    if args.callsignrx in heardmecallsigns:
        print(args.callsignrx + " hears us, activereceiver:", checkactivereceiver(args.callsignrx))
        if args.checkwsjtxall:
            print("in wsjtx all log?:", checkwsjtxalllogsingle(args.callsign))
    else:
        print(args.callsignrx + " doesn't hear us (according to pskreporter), activereceiver:", checkactivereceiver(args.callsignrx))
        if args.checkwsjtxall:
            print("in wsjtx all log?:", checkwsjtxalllogsingle(args.callsign))




