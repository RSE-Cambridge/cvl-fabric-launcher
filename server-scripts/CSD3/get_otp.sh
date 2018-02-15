#!/bin/sh
set -x
#This script should be called from the json file(Strudle)
# to fetch the one time password for the client

module load turbovnc
vncpasswd -o -display localhost:1
