import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCE_PATH = os.path.join(ROOT_PATH, 'resource')
CONFIG_PATH = os.path.join(RESOURCE_PATH, 'config')
SQL_RESOURCE_PATH = os.path.join(RESOURCE_PATH, 'sql')
LOG4J_PROPERTISE_PATH = os.path.join(CONFIG_PATH, 'log4j.properties')
LOG4J_FILE_DESTINATION = "SBDL/app-logs"
LOG4J_DESTINATION_FILENAME = "sbdl-app"

# print(LOG4J_PROPERTISE_PATH)
# print(LOG4J_FILE_DESTINATION)
# print(LOG4J_FILE_DESTINATION)
