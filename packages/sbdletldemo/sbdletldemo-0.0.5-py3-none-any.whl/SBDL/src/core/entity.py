from SBDL.src.core.source import Source
from SBDL.src.core.target import Target
from SBDL.definitions import SQL_RESOURCE_PATH

from SBDL.lib.logger import logger

from pyspark.sql import DataFrame
import os

class Entity:

    sources: list[Source]
    target: Target
    name: str

    def readFromResource(self, file: str) -> str:
        fileWithPath = os.path.join(SQL_RESOURCE_PATH, file)
        query: str = """"""
        with open(fileWithPath, "r") as sqlfile:
            for line in sqlfile:
                if line[len(line)-1] == "\n":
                    line = line[:len(line)-1]
                query += """ {}""".format(line)
        logger.info(query)
        return query

    def transform(self) -> DataFrame:...

    


    

    

