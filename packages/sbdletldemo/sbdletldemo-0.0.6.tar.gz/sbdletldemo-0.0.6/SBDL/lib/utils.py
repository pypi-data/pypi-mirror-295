from SBDL.lib.configLoader import get_spark_conf
from SBDL.definitions import LOG4J_FILE_DESTINATION,LOG4J_DESTINATION_FILENAME,LOG4J_PROPERTISE_PATH

from pyspark.sql import  SparkSession
import os

def get_spark_session():
    EXTRA_JAVA_OPTIONS = """-Dlog4j.configuration=file:{} -Dspark.yarn.app.container.log.dir={} -Dlogfile.name={}""".format(
        LOG4J_PROPERTISE_PATH.replace("\\","/"), 
        LOG4J_FILE_DESTINATION, 
        LOG4J_DESTINATION_FILENAME)
    # print(EXTRA_JAVA_OPTIONS)
    # print('reach here')
    spark = SparkSession.builder \
        .config(conf=get_spark_conf('local')) \
        .config("spark.driver.extraJavaOptions",EXTRA_JAVA_OPTIONS) \
        .master("local[2]") \
        .getOrCreate()
    
    return spark

spark = get_spark_session()
