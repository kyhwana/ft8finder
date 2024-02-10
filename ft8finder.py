#!/usr/bin/python
import adif_io
import xml.etree.ElementTree as ET #rip unstrusted

#TODO: include band based on "frequency" attrib (first two digits?)
#TODO: parse wsjtx_adi to see if i've worked them before
# check the band
#TODO: download files from pskreporter
#TODO: add last heard/seen?
#TODO: optional "they might not be reporting to pskreporter" flag
#TODO: read from "who I heard via _ALL.txt" instead of pskreporter? grep it for the call + time minus my call if it comes after it.
#TODO: add cli command with a callsign and return true/false if we can work them

wsjtxfile = "wsjtx_log.adi"
receivertag = "activeReceiver" #stations that are actively listening
receptionreporttag = "receptionReport" #stations that heard US
activecallsigntag = "activeCallsign" #???
mycallsign = "ZL4KYH" #changeme
mode = "FT8"
heardmecallsigns = [] #callsigns that are hearing me
iheardcallsigns = [] #callsigns i've heard from pskreporter

#https://retrieve.pskreporter.info/query?senderCallsign=CALLSIGN&appcontact=emailaddress" for who heard us.
#  <receptionReport receiverCallsign="WA6OUR-K" receiverLocator="CN87xo" senderCallsign="ZL4KYH" senderLocator="RE78js" frequency="24917631" flowStartSeconds="1707517560" mode="FT8" isSender="1" receiverDXCC="United States" receiverDXCCCode="K" sNR="-17" />

#https://retrieve.pskreporter.info/query?receiverCallsign=CALLSIGN&appcontact=emailaddress for who we heard 
#  <receptionReport receiverCallsign="ZL4KYH" receiverLocator="RE78js" senderCallsign="N7BC" senderLocator="CN87ql20" frequency="24915356" flowStartSeconds="1707517048" mode="FT8" isReceiver="1" senderRegion="Washington" senderDXCC="United States" senderDXCCCode="K" senderDXCCLocator="EM47" senderLotwUpload="2024-02-04" senderEqslAuthGuar="A" sNR="-6" />

#qsos, header = adif_io.read_from_file("test1.adi")
#print("QSOS: {}".format(qsos, header))


rxtree = ET.parse('test2.adi')
txtree = ET.parse('test3rx.adi')
rxroot = rxtree.getroot()
for child in rxroot:
    if child.tag == "receptionReport":
        print(child.tag, child.attrib)
        print("heard me ", child.attrib.get('receiverCallsign'))
        heardmecallsigns.append(child.attrib.get('receiverCallsign'))
txroot = txtree.getroot()
for child in txroot:
    if child.tag == "receptionReport":
        print(child.tag, child.attrib)
        print("I heard ", child.attrib.get('senderCallsign'))
        iheardcallsigns.append(child.attrib.get('senderCallsign'))
workableset = set(heardmecallsigns).intersection(iheardcallsigns)        
workablelist = sorted(workableset)

print(workablelist)

