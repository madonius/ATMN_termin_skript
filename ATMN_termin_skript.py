#!/usr/bin/python3
# -*- coding: utf-8 -*-

#    ATMN Kalender Skript, converts the list of appointments on the atmn.info website
#to an .ics file
#    Copyright (C) 2011 Emmanouil Kampitakis <emmanouil@kampitakis.de>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import re
import shutil
import getopt
import os
import datetime
import time
import random
import urllib.request
import codecs

#return todays date and time in ical format
def returndate():
   return time.strftime("%Y%m%d") + "T" + time.strftime("%H%M%S")+"Z"

#check if the number is single digit and make it so if not
def checkdigits(num):
   if len(num) == 2:
      return num
   else:
      return "0"+num


#DEFINE VERIABLES
FILEDIR='./files'
ICSDIR='./output'
MONTHS='./files/dates.log'

#check for existing files and directories, if they don't exist create them
#fonder to store relevant files #memory
if not os.path.exists(FILEDIR):
   os.makedirs(FILEDIR)
#folder to store the ics files
if not os.path.exists(ICSDIR):
   os.makedirs(ICSDIR)

if not os.path.isfile(MONTHS):
   isdate=0
else:
   isdate=1

#define regex
date  = re.compile("([0-9]+)\.([0-9]+)\.([0-9]{4})")
title = re.compile("([0-9]{3}\. Stammtisch)")

today = datetime.date.today()

#download the webpage
Stammtisch_htm = urllib.request.urlopen("http://atmn.info/Stammtisch.htm")
Stammtischlines_uml = Stammtisch_htm.readlines()
Stammtisch_htm.close

Stammtischlines = [l.decode('windows-1252') for l in Stammtischlines_uml]

outputheader=['BEGIN:VCALENDAR','PRODID:ATMN','VERSION:2.0','CALSCALE:GREGORIAN','METRO:PUBLISH','X-WR-CALNAME:ATMN-Stammtische'+time.strftime("%W")+'Woche','X-WR-TIMEZONE:Europe/Berlin','X-WR-CALDESC:ATMN Stammtisch' +time.strftime("%W") +' Woche']

output=[]
output.extend(outputheader)
#checks prexistence and opens the dates.log file 
if isdate == 1:
   log = open(MONTHS,"r+")
   log_mem = log.read()
else:
   log = open(MONTHS,"a+")

for line in range(0,len(Stammtischlines)-1):
   print(line)
   if(title.search(Stammtischlines[line]) == 1):
      eventtitle = title.search(line)[0]
      eventdate  = date.search(line+2)
      
      eventdate_day   = checkdigits(eventdate[0])
      eventdate_month = checkdigits(eventdate[1])
      eventdate_year  = eventdate[2]

      if((isdate==0) or (log_mem.find(str(eventdate_year) + str(eventdate_month) + str(eventdate_day)) == -1)):
         output.append('BEGIN:VEVENT')
         output.append('DTSTART;TZID=Europe/Berlin:'+eventdate_year+eventdate_month+eventdate_day+'T190000Z')
         output,append('DURATION:PT04H00M00S')
         output.append('DTSTAMP:'+returndate())
         output.append('UID:atmn'+str(random.random()+random.random())+time.strftime("%W",time.gmtime())+"week@atmn.info")
         output.append('CREATED:'+returndate())
         output.append('DESCRIPTION: '+eventtitle)
         output.append('LOCATION:Hotel und Tafernwirtschaft, Fischer, Bahnhofstrasse 4, 85221 Dachau')
         output.append('SEQUENCE:0')
         output.append('STATUS:TENTATIVE')
         output.append('SUMMARY: Um vollmond rum treffen wir uns immer zu einem ungezwungenen Stammtisch')
         output.append('TRANSP:OPAQUE')
         output.append('END:VEVENT')

         #define logfiles ti write out the days already parsed and written
         log.write(str(eventdate_year)+str(eventdate_month)+str(eventdate_day)+"\n")

#close te log file
log.close()
#close the calendat
output.append('END:VCALENDAR')

#output if the File
print("output file created",file=sys.stderr)

OUTPUTFILE=ICSDIR+"/output"+time.strftime("%Y%m%d")+".ics"
if not os.path.isfile(OUTPUTFILE):
   print("writing file", file=sys.stderr)
   output_file = open(UOTPUTFILE,"w", encoding="utf-8")
   output_file.write('\r\n'.join(output))
   output_file.close()
