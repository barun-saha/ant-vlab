# globals.py
# Define global constants
# (Rev #27: #1)

from django.conf import settings

NS2_PATH = '/usr/local/bin/ns'
NS3_INSTALL_PATH = '/home/barun/Desktop/ns3/ns-allinone-3.10/ns-3.10'
BASH_PATH = '/bin/bash'

if settings.__ENV_PROD__:
    # Prod
    NS2_SCRIPT_STORAGE_PATH = '/var/vlabs/ant'
    NS3_SCRIPT_STORAGE_PATH = '/var/vlabs/ant/ns3'
    NS3_HELPER_PATH = '/home/barun/codes/www/vlabs/ns3helper.sh'
    NS3_SYM_LINK = 'ns3ant'
    
    # (Rev #35: #1)    
    WIMAX_REF_PATH = '/var/vlabs/ant/_wimax_ref_'
    #WIMAX_REF_FILES = ( 'PED_A', 'PED_B', 'BetaTable.txt', 'BLER_LookupTable.txt', )
else:
    # Dev
    NS2_SCRIPT_STORAGE_PATH = '/var/vlabs_demo/ant'
    NS3_SCRIPT_STORAGE_PATH = '/var/vlabs_demo/ant/ns3'
    NS3_HELPER_PATH = '/home/barun/codes/svn_chkout/ant/20Aug2011/trunk/vlabs/ns3helper.sh'
    NS3_SYM_LINK = 'ns3ant_demo'
    
    # (Rev #35: #1)
    WIMAX_REF_PATH = '/var/vlabs_demo/ant/_wimax_ref_'
    #WIMAX_REF_FILES = ( 'PED_A', 'PED_B', 'BetaTable.txt', 'BLER_LookupTable.txt', )
