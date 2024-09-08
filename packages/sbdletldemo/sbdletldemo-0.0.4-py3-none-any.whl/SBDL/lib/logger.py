from SBDL.lib.utils import get_spark_session


class Log4J(object):
    def __init__(self):
        spark = get_spark_session()
        log4j = spark._jvm.org.apache.log4j
        self.logger = log4j.LogManager.getLogger("sbdl")
    
    def warn(self, message) -> None:
        self.logger.warn(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)

logger = Log4J()