from SBDL.src.core.entity import Entity
from SBDL.src.core.source import LocalSource
from SBDL.src.core.target import LocalTarget

from SBDL.lib.logger import logger
from SBDL.lib.utils import spark

from pyspark.sql import DataFrame

class CustLoad(Entity):
    name: str = "CustLoad"

    sources = [
        LocalSource("dbfs:/FileStore/aakashverma/employee/read", "csv",",", "raw_employee", True)
    ]

    target = LocalTarget("dbfs:/FileStore/aakashverma/employee/write","csv", repartition=4)

    def transform(self)-> DataFrame:
        logger.info("Reading employees table")
        df = spark.sql(self.readFromResource("read_employee.sql"))
        logger.info("Showing employees table")
        df.show()
        return df

