from  SBDL.lib.utils import get_spark_session
from  SBDL.lib.logger import logger

from SBDL.src.core.publisher import Publisher

import sys


def main(argv):
    publisher = Publisher()
    publisher.run(sys.argv[1])



# if __name__ == "__main__":
#     if(len(sys.argv)<2):
#         print("Usage: sbdl {entity_name}: Arguments are missing")
#         '''
#         "{\"entity\":\"acctload\"}"
#         '''
#         sys.exit(-1)
#     main(sys.argv)
