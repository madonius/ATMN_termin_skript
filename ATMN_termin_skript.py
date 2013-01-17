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

def returndate():
   return time.strftime("%Y%m%d") + "T" + time.strftime("%H%M%S")+"Z"

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

if not os.path.isfile('./files/dates.log'):
   isdate=0
else
   isdate=1

#define regex
date  = re.compile("([0-9]+)\.([0-9]+)\.([0-9]{4})")
title = re.compile("([0-9]{3})\.")

today = datetime.date.today()

#download the webpage
Stammtisch_htm = urllib.request.urlopen("http://atmn.info/Stammtisch.htm")
Stammtischlines = Stammtisch_htm.readlines()
Stammtisch_htm.close



