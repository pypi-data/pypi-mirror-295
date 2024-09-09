from SBDL.main_sbdl import main as sbdl_main
from SBDL.lib.logger import logger

import sys

def main(argv):
    sbdl_main(argv)

if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("Usage: sbdl {entity_name}: Arguments are missing")
        '''
        "{\"entity\":\"acctload\"}"
        '''
        sys.exit(-1)
    logger.info(sys.argv)
    main(sys.argv)