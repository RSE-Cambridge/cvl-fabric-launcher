#!/bin/bash

# Utility for packaging the Linux version of the installer.
#
# You may have to change PYINSTALLERDIR to point to the directory where
# pyinstaller was unpacked.

PYINSTALLERDIR=`pwd`/pyinstaller

set -o nounset
set -e

VERSION=`grep '^version_number' launcher_version_number.py | cut -f 2 -d '"'`
ARCHITECTURE=`uname -m | sed s/x86_64/amd64/g | sed s/i686/i386/g`

rm -fr dist

python create_commit_def.py

# PyInstaller 2.1
PATHS=`python -c 'import appdirs ; import os ; print os.path.dirname(appdirs.__file__)'`
python ${PYINSTALLERDIR}/pyinstaller.py --paths=$PATHS launcher.py

cp "Strudel.desktop" 	dist/launcher/
cp strudel.sh 		dist/launcher/

mkdir dist/launcher/icons
cp IconPngs/* dist/launcher/icons/
cp README_LINUX dist/launcher/
cp -r cvlsshutils dist/launcher/

cp `python -c 'import requests; print requests.certs.where()'` dist/launcher/

mkdir -p dist/launcher/help/helpfiles/
cp help/helpfiles/* dist/launcher/help/helpfiles/
cp help/README.txt dist/launcher/help/
cp masterList.url dist/launcher/

mkdir dist/Strudel-${VERSION}_${ARCHITECTURE}
cp README_LINUX  dist/Strudel-${VERSION}_${ARCHITECTURE}
cp strudel.sh    dist/Strudel-${VERSION}_${ARCHITECTURE}
mv dist/launcher dist/Strudel-${VERSION}_${ARCHITECTURE}/bin

cd dist
tar zcf Strudel_v${VERSION}_${ARCHITECTURE}.tar.gz Strudel-${VERSION}_${ARCHITECTURE}
cd ..

ls -lh dist/Strudel_v${VERSION}_${ARCHITECTURE}.tar.gz

