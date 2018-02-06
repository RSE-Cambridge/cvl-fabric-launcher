#!/bin/bash

SRC=`pwd`

VERSION=`grep '^version_number' ${SRC}/launcher_version_number.py | cut -f 2 -d '"'`
ARCHITECTURE=`uname -m | sed s/x86_64/amd64/g | sed s/i686/i386/g`

./package_linux_version.sh

cd rpmbuild

rm -fr BUILD BUILDROOT RPMS SOURCES SRPMS tmp
mkdir  BUILD BUILDROOT RPMS SOURCES SRPMS tmp

rm -f ~/.rpmmacros
echo "%_topdir  "`pwd`     >> ~/.rpmmacros
echo "%_tmppath "`pwd`/tmp >> ~/.rpmmacros


sed s/VERSION/${VERSION}/g SPECS/strudel.spec.template > SPECS/strudel.spec

if [ "$ARCHITECTURE" == "amd64" ]
then
    sed -i s/libc.so.6\(GLIBC_PRIVATE\)/libc.so.6\(GLIBC_PRIVATE\)\(64bit\)/g SPECS/strudel.spec
fi

rm -fr strudel-${VERSION}

mkdir -p strudel-${VERSION}/opt/Strudel
mkdir -p strudel-${VERSION}/usr/share/applications
rm -f strudel-${VERSION}.tar.gz SOURCES/strudel-${VERSION}.tar.gz 

cp ../Strudel.desktop strudel-${VERSION}/usr/share/applications/
cp -r ../dist/Strudel-${VERSION}_${ARCHITECTURE}/* strudel-${VERSION}/opt/Strudel

tar zcf strudel-${VERSION}.tar.gz strudel-${VERSION}
cp strudel-${VERSION}.tar.gz SOURCES/

rpmbuild -ba SPECS/strudel.spec
cd ..

find rpmbuild/ -iname '*rpm' -exec ls -lh {} \;


