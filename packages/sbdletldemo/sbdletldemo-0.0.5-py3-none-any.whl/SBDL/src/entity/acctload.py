from SBDL.src.core.entity import Entity
from SBDL.src.core.source import LocalSource
from SBDL.src.core.target import LocalTarget

from SBDL.lib.logger import logger
from SBDL.lib.utils import spark

from pyspark.sql import DataFrame

class AcctLoad(Entity):
    name: str = "AcctLoad"

    sources = [
        LocalSource("D:/projects/SBDL-Workspace/test_data/read", "csv",",", "raw_employee", True)
    ]

    target = LocalTarget("D:/projects/SBDL-Workspace/test_data/read","csv", repartition=4)

    def transform(self)-> DataFrame:
        logger.info("Reading employees table")
        df = spark.sql(self.readFromResource("read_employee.sql"))
        logger.info("Showing employees table")
        df.show()
        return df

