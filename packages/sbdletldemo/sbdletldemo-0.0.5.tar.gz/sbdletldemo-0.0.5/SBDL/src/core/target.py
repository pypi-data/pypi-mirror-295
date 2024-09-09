
from pyspark.sql import DataFrame

class SaveMode:
    OverWrite : str = "overwrite"

saveMode = SaveMode()

class Target:
    def write(self, df: DataFrame):...

class LocalTarget(Target):
    def __init__(self, path, filetype, header: bool = True, repartition: int = 0):
        self.path = path
        self.filetype = filetype
        self.header = header
        self.repartition = repartition
    
    def write(self, df: DataFrame):
        # df.write.format("csv")
        df.repartition((self.repartition, df.rdd.getNumPartitions())[self.repartition==0]) \
            .write \
            .mode(saveMode.OverWrite) \
            .format(self.filetype) \
            .option("header", self.header) \
            .save(self.path)



    