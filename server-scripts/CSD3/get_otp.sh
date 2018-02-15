#!/bin/sh
set -x

module load turbovnc
vncpasswd -o -display localhost:1
