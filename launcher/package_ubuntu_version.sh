#!/bin/bash

VERSION=`grep '^version_number' launcher_version_number.py | cut -f 2 -d '"'`
ARCHITECTURE=`uname -m | sed s/x86_64/amd64/g | sed s/i686/i386/g`

./package_linux_version.sh $VERSION $ARCHITECTURE

TMP="tmp_debian_build"

alias sudo=""
sudo rm -fr $TMP
sudo rm -f *.deb

TARGET=$TMP/opt/Strudel
mkdir -p $TARGET

mkdir -p $TMP/usr/share/applications

cp Strudel.desktop $TMP/usr/share/applications/

cp -r dist/Strudel-${VERSION}_${ARCHITECTURE}/* $TARGET/
mkdir $TMP/DEBIAN
cp release/control  $TMP/DEBIAN
# This is not necessary on Ubuntu 13.04 when building for Ubuntu
# cp release/postinst $TMP/DEBIAN

# Remove pango from the control file, not needed on Ubuntu 13
sed -i 's/libpango1.0-dev,//g' $TMP/DEBIAN/control


installedSize=`du -sx --exclude DEBIAN $TMP | awk '{print $1}'`

sed -i "s/VERSION/${VERSION}/g" $TMP/DEBIAN/control
sed -i "s/ARCHITECTURE/${ARCHITECTURE}/g" $TMP/DEBIAN/control
sed -i "s/XXINSTALLEDSIZE/${installedSize}/g" $TMP/DEBIAN/control

sudo chown -R root.root $TMP
sudo find $TMP/ -iname '*.so.*' -exec chmod a-x {} \;
sudo find $TMP/ -iname '*.so.*' -exec strip     {} \;
mkdir -p $TMP/opt/Strudel/icons/
cp IconPngs/MASSIVElogoTransparent144x144.png  $TMP/opt/Strudel/icons/MASSIVElogoTransparent144x144.png
cp Strudel.desktop $TMP/opt/Strudel/"Strudel.desktop"
sudo chmod a-x $TMP/opt/Strudel/icons/MASSIVElogoTransparent144x144.png
sudo chmod a-x $TMP/opt/Strudel/"Strudel.desktop"

DEB=strudel_UBUNTU_${VERSION}_${ARCHITECTURE}.deb
sudo dpkg -b $TMP $DEB

echo
echo
echo
ls -lh *.deb
echo
echo
