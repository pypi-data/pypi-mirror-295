import configparser
from pyspark import SparkConf
import os

from SBDL.definitions import CONFIG_PATH

def get_config(env):
    pass


def get_spark_conf(env):
    conf_file = os.path.join(CONFIG_PATH,"spark.conf")
    spark_conf = SparkConf()
    config = configparser.ConfigParser()
    config.read(conf_file)

    for (key, val) in config.items(env):
        spark_conf.set(key, val)
    return spark_conf