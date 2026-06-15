#!/bin/bash
DIR=$(cd `dirname $0` && pwd)
PYROPATH=$(cd `dirname $0` && cd .. && pwd)

# Install build dependencies (if needed)
if [ ! -f /usr/bin/debuild ];
then
    sudo apt-get install devscripts equivs python-setuptools dh-python
fi
if [ ! -f /usr/bin/rpm ];
then
    sudo apt-get install rpm
fi
if [ ! -f /usr/lib/python3/dist-packages/sphinxarg/ext.py ];
then
    sudo apt install python3-sphinx-argparse
fi

# Update pyromaths version
VERSION=`date +%y.%-m`
echo "What is the current version number? (Default: ${VERSION})"
read touche
case "$touche" in
  "" )
  ;;
  * )
  VERSION="$touche"
  ;;
esac
echo "*** Update pyromaths version..."
sed -i "s/VERSION ?= .*/VERSION ?= ${VERSION}/" ${PYROPATH}/Makefile

# Clean-up and create Documentation
cd $PYROPATH/Doc
make clean
make doctest
make html

# Prepare Changelog
cd $PYROPATH
head -20 NEWS
dch -v ${VERSION}-1
dch -r

# Clean-up and create packages
make clean
make all
make repo

echo "*** Tag git develop ***"
echo "Do you want to commit and tag the git develop branch (o/N)?"
read touche
case "$touche" in
  [oO] )
  git commit -am "Pyromaths Release version ${VERSION}"
  git tag -u B39EE5B6 version-${VERSION} -m "Pyromaths ${VERSION}"
  #git push --tags:
  ;;
esac
