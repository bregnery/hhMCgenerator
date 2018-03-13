#!/bin/bash

#script to run generic lhe generation tarballs
#kept as simply as possible to minimize need
#to update the cmssw release
#(all the logic goes in the run script inside the tarball
# on frontier)
#J.Bendavid

#exit on first error
set -e

echo "   ______________________________________     "
echo "         Running Generic Tarball/Gridpack     "
echo "   ______________________________________     "

path=${1}
echo "gridpack tarball path = $path"

nevt=${2}
echo "%MSG-MG5 number of events requested = $nevt"

rnum=${3}
echo "%MSG-MG5 random seed used for the run = $rnum"

echo "%MSG-MG5 residual arguments = ${@:4}"

LHEWORKDIR=`pwd`

if [[ -d lheevent ]]
    then
    echo 'lheevent directory found'
    echo 'Setting up the environment'
    rm -rf lheevent
fi
mkdir lheevent; cd lheevent

#copy locally
xrdcp ${path} gridpack_tarball.tar.xz 

#untar the tarball
tar -xaf gridpack_tarball.tar.xz 

#get permission to execute the run file
chmod a+x runcmsgrid.sh

#generate events (call for 1 core always for now until hooks to set number of cores are implemented upstream)
./runcmsgrid.sh $nevt $rnum 1 #${@:4}

mv cmsgrid_final.lhe $LHEWORKDIR/

cd $LHEWORKDIR

#cleanup working directory (save space on worker node for edm output)
rm -rf lheevent

exit 0

