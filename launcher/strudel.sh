#!/bin/bash

# get directory of strudel
# this returns the correct absolute path to itself no matter how this script is called:
# absolute/relative path, direct/nested symlink, script/symlink in $PATH and more ... 
SOURCE="${BASH_SOURCE[0]}" # for zsh this would be: SCRIPT_PATH=${(%):-%N}
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  STRUDEL_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  [[ $SOURCE != /* ]] && SOURCE="$STRUDEL_DIR/$SOURCE" 
done
STRUDEL_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

## --- This can be a fix for systems, where libgio-2.0 is different to the build environment ---
## add included libgio if not avail on system - use system if avail
#LIBGIO_PATH=$(/sbin/ldconfig -p | grep  libgio-2.0.so.0)
#if [ -z "$LIBGIO_PATH" ]; then
#  echo "WARNING: libgio-2.0.so.0 not found on system - using build in version"
#  LD_LIBRARY_PATH="${STRUDEL_DIR}"/bin/libgio:$LD_LIBRARY_PATH
#fi

if [ -f "${STRUDEL_DIR}"/launcher ]; then
  LD_LIBRARY_PATH="${STRUDEL_DIR}":$LD_LIBRARY_PATH
  "${STRUDEL_DIR}"/launcher > ${HOME}/.strudel.log 2>&1
elif [ -f "${STRUDEL_DIR}"/bin/launcher ]; then
  LD_LIBRARY_PATH="${STRUDEL_DIR}/bin":$LD_LIBRARY_PATH
  "${STRUDEL_DIR}"/bin/launcher > ${HOME}/.strudel.log 2>&1
else
  echo "ERROR: Cannot find launcher."
fi
