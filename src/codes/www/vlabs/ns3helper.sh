#!/bin/bash

NS3_INSTALLATION_DIR=/home/barun/Desktop/ns3/ns-allinone-3.10/ns-3.10

if [[ $# -ne 1 ]];
then
    echo "Missing argument: filename"
    exit 1
fi
SCRIPT_FILE_NAME="$1"

# This is the * most * important step; ./waf wont work otherwise
cd "$NS3_INSTALLATION_DIR"

# For Dev
#./waf --run "ns3ant_demo/$SCRIPT_FILE_NAME" 2>&1 | sed 's/\/home\/barun\/Desktop\/ns3\/ns-allinone-3.10/NS3PATH/g'
#./waf --run "ns3ant_demo/$SCRIPT_FILE_NAME" 2>&1 | grep -Ev 'Entering directory|Leaving directory|cxx: ns3|cxx_link:'
# For Prod
#./waf --run "ns3ant/$SCRIPT_FILE_NAME" 2>&1 | sed 's/\/home\/barun\/Desktop\/ns3\/ns-allinone-3.10/NS3PATH/g'
./waf --run "ns3ant/$SCRIPT_FILE_NAME" 2>&1 | grep -Ev 'Entering directory|Leaving directory|cxx: ns3|cxx_link:'
