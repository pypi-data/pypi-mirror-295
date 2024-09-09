import sys
from SBDL.main_sbdl import main

def on_databricks():
    print("--------------------------------------")
    print("Running Wheel Atleast")
    print(sys.argv)
    if(len(sys.argv)<2):
        print("Usage: sbdl {entity_name}: Arguments are missing")
        '''
        "{\"entity\":\"acctload\"}"
        '''
        sys.exit(-1)
    main(sys.argv)
    print("---------------------------------------------")